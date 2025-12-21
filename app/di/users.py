from dishka import Provider, Scope, provide

from app.core.users.interactor import GetUsersInteractor


class UsersProvider(Provider):
    scope = Scope.REQUEST

    get_users = provide(GetUsersInteractor)
