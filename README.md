
## Архитектура и композиция файлов в FastApi приложении
![](https://habrastorage.org/webt/aq/ck/-d/aqck-dopofu_gkewbmurdj5plgo.jpeg)
![enter image description here](https://habrastorage.org/webt/ln/ul/_g/lnul_gxx7h81f8kdhebmlbdue24.png)

## Описание папок и файлов
### **API**
В папке API находятся два типа файлов Depends и Routers <br>
- Depends - функции-зависимости которые выполняются до момента получения данных в Router.
- Routers - Endpoint-ы которые принимают данные и валидируют данные от клиента.

**Все файлы именуются по предметной области** <br>

### **Apps** 
Взято из практики Django Apps. В данной папке находятся модули системы разделенные на предметные области.
> Apps/accounts - Папка с файлами которая отвечает за модуль системы работающий с accounts

В данную папку входит

    - logic.py  # Работа с бизнес-логикой
    - crud.py  # Работа с БД
    - models.py  # Схема БД
    - utils.py
    - enums.py  # опционально
    - schemas.py   # Pydantic-схемы опционально

### **Core**
Находятся основные файлы системы которые регулируют работу приложения. <br>
В данную папку входит
   
    - config.py  # Все настройки и параметры приложения
    - main.py  # Главный модуль приложения FastApi object
    - middleware.py
    - scheduler.py  # CRON задачи приложения
    - urls.py

### **DB**
Находятся конфигурационные параметры и настройки БД
### **Enums**
Выделены отдельной папкой на практике показало более удобное использование Enums и переиспользование их в других модулях.
Для опрд. систем enum можно выделить в самом App. <br>
**Все файлы именуются по предметной области** <br>

### **Schemas**
Выделены отдельной папкой на практике показало более удобное использование Schemas и переиспользование их в других модулях.
Для опрд. систем schemas можно выделить в самом App. <br>
**Все файлы именуются по предметной области** <br>

### **Submodules**
Изолированные модули системы представляют собой аналогичные папки из Apps.
Могут быть как какие-нибудь исходники, библиотеки и т.д.

## Как взаимодействуют слои между собой
**Контроллеры** - Предназначены для валидации входных данных, приема и передачи данных из бизнес слоя.
- Входные данные - Pydantic объект или примитивные типы
- Выходные данные - Pydantic объект

> Core > urls.py - Файл для подключения всех router-ов приложения

    from src.api.routers.accounts import router as account_router
    
    api_router = APIRouter()
    
    api_router.include_router(account_router, tags=["accounts"])
    ...

> Api > routers > accounts.py - Файл с router для предметной области accounts

    @router.post("/")
    async  def  create_account(account_create:  AccountCreate)  ->  AccountData:
	    return  await  account_logic.create_account(account_create)

> Api > depends > accounts.py - Набор функций-зависимостей которые работают с accounts


----
**Бизнес-логика** - Предназначена для работы с бизнес-задачами, внутренними процессами системы, приемом и передачей данных из слоя по работе с БД.
- Входные данные - Pydantic объект или примитивные типы
- Выходные данные - Pydantic объект

> Apps > accounts > logic.py - Файл с бизнес-логикой по работе с accounts

    async  def  create_account(account_create:  AccountCreate)  ->  AccountData:
	    account  =  await  accounts_crud.create(account_create)
	    return  AccountData.from_orm(account)

----
**Доступ к данным БД** - Предназначен для работы выполнения операций в БД.
- Входные данные - Pydantic объект или примитивные типы
- Выходные данные - Объект модели

> Apps > accounts > crud.py - Файл выполнению операций в БД для таблицы Accounts

    async def create(account_create: AccountCreate) -> Account:
        return await Accounts.create(**data.dict())

![](https://habrastorage.org/webt/pu/r-/e7/pur-e7zc4o4_s-lol43qmsu0mfm.png)

####  Данная композиция файлов была внедрена и протестирована на нескольких коммерческих проектов.

