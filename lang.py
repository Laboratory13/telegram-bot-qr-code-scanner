


class Lang:
    class ru:
        abr             = "ru"
        wellcome        = "Привет, это бот помошник продавец!\nПожалуйста поделитесь с контактом для продолжения."
        share_contact   = "Поделиться c контактом"
        please_contact  = "Поделитесь с контактом для регистрации!"
        lang            = "🇷🇺 Русский 🇷🇺"
        done            = "Сделано!"
        settings        = "Настройки"
        check           = "Проверить-QR"
        instructions    = "Инструкции"
        contact_us      = "Контакты"
        send_photo      = "Отправьте фото QR-кода"
        contacts        = "Здесь контакты текст примерно\nдва или\nтри строки"
        menu            = "Меню"
        accept          = "Принять"
        reject          = "Отказать"
        specify         = "Напишите причину отказа"
        send_proove     = "Отправьте фото продукта с клиентом"
        send_desc       = "Отправьте описание"
        not_found       = "QR-код не прочитан"
        upload_photo    = "Пожалуйста отправьте фото!"
        photo_desc      = "Опишите продажу"
        alrd_uploded    = "Фото уже отправлено"
        send_video      = "Отправьте видео-инструкцию"
        change_video    = "Изменить инструкцию"
        not_finished    = "Закончите задачу!"
        close           = "Отменить"
        closed          = "Отменено"
        get_team        = "Список продавцов"
        skip            = "Пропустить"
        reason          = "Напишите причину отказа"
        prod_name       = "Наименования продукта"
        prod_desc       = "Описание продукта"
        client          = "Клиент"
        order_time      = "Время заказа"
        phone           = "Тел"
        price           = "Цена за продукт"
        prod_not_found  = "Продукт не найден"
        prod_sold       = "Продукт уже был выдан"
        last            = "Не понимаю!"


    class uz(ru):
        abr             = "uz"
        wellcome        = "Salom bu bot sotuvchi yordamchisi!\n"
        share_contact   = "Kontaktni jo'natish"
        please_contact  = "Registratsiya uchun kontaktingizni jo'nating!"
        lang            = "🇺🇿 O'zbekcha 🇺🇿"
        done            = "Bajarildi!"
        settings        = "Sozlamalar"
        check           = "QR-Tekshirish"
        instructions    = "Qo'llanma"
        contact_us      = "Bog'lanish"
        send_photo      = "QR-kod rasmini jo'nating"
        contacts        = "Bu yerda kompaniya\nkontaktlari bo'ladi\nTaxminan 2-3 qator"
        menu            = "Asosiy menyu"
        accept          = "Qabul qilish"
        reject          = "Rad etish"
        specify         = "Rad etish sabaini ko'rsating"
        send_proove     = "Mahsulot va mijozning rasmini jo'nating"
        send_desc       = "Tavsilotlarni yozib yuboring"
        not_found       = "QR-kod o'qilmadi"
        upload_photo    = "Iltimos rasmni jo'nating!"
        photo_desc      = "Sotuvni tariflang"
        alrd_uploded    = "Rasm oldin jo'natilgan!"
        send_video      = "Video-qo'llanmani jo'nating"
        change_video    = "Qo'llanmani o'zgartirish"
        not_finished    = "Vazifani tugating!"
        close           = "Tugatish"
        closed          = "Tugatildi"
        get_team        = "Sotuvchilar royxati"
        skip            = "O'tkazib yuborish"
        reason          = "Rad etish sababini kiriting"
        prod_name       = "Tovar yoki xizmat nomi"
        prod_desc       = "Tovar ta'rifi"
        client          = "Mijoz"
        order_time      = "Buyurtma vaqti"
        phone           = "Tel"
        price           = "Tovar yoki xizmat narxi"
        prod_not_found  = "Tovar yoki xizmat topilmadi"
        prod_sold       = "Xizmat oldin ko'rsatilgan"
        last            = "Tushunmadim!"

        
        


    def gl(self, lan_str:str) -> ru:
        if lan_str == "ru":
            return self.ru
        elif lan_str == "uz":
            return self.uz
        return self.ru

    def gal(self, field:str):
        return [
            self.ru.__getattribute__(self.ru, field),
            self.uz.__getattribute__(self.uz, field)
        ]
lang = Lang()