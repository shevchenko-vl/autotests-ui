from enum import StrEnum
from typing import Self, Annotated

from pydantic import EmailStr, FilePath, HttpUrl, DirectoryPath, BaseModel, BeforeValidator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Browser(StrEnum):
    WEBKIT = 'webkit'
    FIREFOX = 'firefox'
    CHROMIUM = 'chromium'


class TestUser(BaseModel):
    email: EmailStr
    username: str
    password: str


class TestData(BaseModel):
    image_png_file: FilePath


def ensure_file_exists(file: FilePath | str) -> FilePath:
    if isinstance(file, str):
        file = FilePath(file)

    file.touch(exist_ok=True)
    return file


def ensure_dir_exists(directory: DirectoryPath | str) -> DirectoryPath:
    if isinstance(directory, str):
        directory = DirectoryPath(directory)

    directory.mkdir(exist_ok=True)
    return directory


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        env_nested_delimiter='.',
    )

    app_url: HttpUrl
    headless: bool
    browsers: list[Browser]
    test_user: TestUser
    test_data: TestData
    videos_dir: Annotated[DirectoryPath, BeforeValidator(ensure_dir_exists)] = DirectoryPath('videos')
    tracing_dir: Annotated[DirectoryPath, BeforeValidator(ensure_dir_exists)] = DirectoryPath('tracing')
    browser_state_file: Annotated[FilePath, BeforeValidator(ensure_file_exists)] = FilePath('browser-state.json')


settings = Settings()
