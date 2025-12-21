from dishka import Provider, Scope, provide

from app.core.users.interactor import GetUsersInteractor, UserByTgIdFinder


class UsersProvider(Provider):
    scope = Scope.REQUEST

    get_users = provide(GetUsersInteractor)
    user_finder = provide(UserByTgIdFinder)
