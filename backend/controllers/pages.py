import msgspec
from litestar import Controller, get


class HomeProps(msgspec.Struct):
    title: str
    message: str


class PagesController(Controller):
    @get(path="/", component="Home")
    async def home(self) -> HomeProps:
        return HomeProps(
            title="Subscription Server",
            message="Litestar drives the page, Svelte renders it.",
        )

    @get(path="/auth", component="Auth")
    async def auth(self) -> AuthProps:
        return HomeProps(
            title="Subscription Server",
            message="Litestar drives the page, Svelte renders it.",
        )
