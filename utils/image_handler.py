import os
import shutil
from PIL import Image
from typing import Optional


class ImageHandler:
    """Класс для работы с изображениями товаров"""

    def __init__(self, images_folder: str = "images"):
        self.images_folder = images_folder
        self.default_image = "resources/picture.png"
        self._create_images_folder()

    def _create_images_folder(self):
        """Создание папки для изображений"""
        if not os.path.exists(self.images_folder):
            os.makedirs(self.images_folder)

    def resize_image(self, image_path: str, size: tuple = (300, 200)) -> Image.Image:
        """Изменение размера изображения"""
        img = Image.open(image_path)
        # Конвертируем в RGB если нужно (для PNG с прозрачностью)
        if img.mode in ("RGBA", "LA"):
            background = Image.new("RGB", img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[-1] if img.mode == "RGBA" else None)
            img = background
        img = img.resize(size, Image.Resampling.LANCZOS)
        return img

    def save_product_image(self, source_path: str, product_id: int) -> str:
        """
        Сохранение изображения товара
        Возвращает путь к сохраненному изображению
        """
        if not source_path or not os.path.exists(source_path):
            return self.default_image

        # Формируем имя файла
        extension = os.path.splitext(source_path)[1].lower()
        if extension not in [".jpg", ".jpeg", ".png", ".bmp"]:
            extension = ".jpg"

        filename = f"product_{product_id}{extension}"
        destination = os.path.join(self.images_folder, filename)

        try:
            # Изменяем размер и сохраняем
            img = self.resize_image(source_path)
            img.save(destination, quality=85)
            return destination
        except Exception as e:
            print(f"Ошибка при сохранении изображения: {e}")
            return self.default_image

    def delete_image(self, image_path: str):
        """Удаление изображения"""
        if (
            image_path
            and image_path != self.default_image
            and os.path.exists(image_path)
            and self.images_folder in image_path
        ):
            try:
                os.remove(image_path)
            except Exception as e:
                print(f"Ошибка при удалении изображения: {e}")

    def get_default_image_path(self) -> str:
        """Получение пути к изображению-заглушке"""
        if os.path.exists(self.default_image):
            return self.default_image
        return ""
