import base64
import cloudinary
import qrcode
import io
import cloudinary.uploader

from sqlalchemy.orm import Session

from src.database.models import Photo
from src.conf.config import cloudinary_config
from src.schemas_of_transformation import TransformerModel


async def transformer(photo_id: int, body: TransformerModel, db: Session) -> Photo | None:

    #post = db.query(Photo).filter(Photo.user_id == user.id, Photo.id == photo_id).first()
    photo = db.query(Photo).filter(Photo.id == photo_id).first()
    if photo:
        transformation = []

        if body.circle.use_filter and body.circle.height and body.circle.width:
            trans_list = [{'gravity': "face", 'height': f"{body.circle.height}", 'width': f"{body.circle.width}",
                           'crop': "thumb"},
                          {'radius': "max"}]
            [transformation.append(elem) for elem in trans_list]

        if body.effect.use_filter:
            effect = ""
            if body.effect.art_audrey:
                effect = "art:audrey"
            if body.effect.art_zorro:
                effect = "art:zorro"
            if body.effect.blur:
                effect = "blur:300"
            if body.effect.cartoonify:
                effect = "cartoonify"
            if effect:
                transformation.append({"effect": f"{effect}"})

        if body.resize.use_filter and body.resize.height and body.resize.height:
            crop = ""
            if body.resize.crop:
                crop = "crop"
            if body.resize.fill:
                crop = "fill"
            if crop:
                trans_list = [{"gravity": "auto", 'height': f"{body.resize.height}", 'width': f"{body.resize.width}",
                               'crop': f"{crop}"}]
                [transformation.append(elem) for elem in trans_list]

        if body.text.use_filter and body.text.font_size and body.text.text:
            trans_list = [{'color': "#FFFF00",
                           'overlay': {'font_family': "Times", 'font_size': f"{body.text.font_size}",
                                       'font_weight': "bold", 'text': f"{body.text.text}"}},
                          {'flags': "layer_apply", 'gravity': "south", 'y': 20}]
            [transformation.append(elem) for elem in trans_list]

        if body.rotate.use_filter and body.rotate.width and body.rotate.degree:
            trans_list = [{'width': f"{body.rotate.width}", 'crop': "scale"}, {'angle': "vflip"},
                          {'angle': f"{body.rotate.degree}"}]
            [transformation.append(elem) for elem in trans_list]

        if transformation:
            cloudinary_config()
            url = cloudinary.CloudinaryImage(f'PhotoShareApp/"current_user.username"').build_url(
                transformation=transformation
            )
            photo.qr_code_url = url
            db.commit()

        return photo


def show_qr_code(photo_id: int, db: Session) -> str | None:

    #photo = db.query(Photo).filter(Photo.user_id == user.id, Photo.id == photo_id).first()
    photo = db.query(Photo).filter(Photo.id == photo_id).first()
    if photo:
        if photo.qr_code_url:
            qr_image = qrcode.make(photo.qr_code_url)
            cloudinary_config()
            qr = cloudinary.uploader.upload(qr_image, public_id='qr_code', overwrite=True)
            qr_url = cloudinary.CloudinaryImage(f'PhotoShareApp/"current_user.username"') \
                .build_url(width=250, height=250, crop='fill', version=qr.get('version'))

            return qr_url
