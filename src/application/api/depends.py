from application.domain.auth.use_cases.authenticate_user import (
    AuthenticateUserUseCase,
)
from application.domain.auth.use_cases.create_access_token import (
    CreateAccessTokenUseCase,
)
from application.domain.category.use_cases.create_category import (
    CreateCategoryUseCase,
)
from application.domain.category.use_cases.delete_category import (
    DeleteCategoryUseCase,
)
from application.domain.category.use_cases.get_category import (
    GetCategoryUseCase,
)
from application.domain.category.use_cases.get_category_admin import (
    GetCategoryAdminUseCase,
)
from application.domain.category.use_cases.get_category_posts import (
    GetCategoryPostsUseCase,
)
from application.domain.category.use_cases.get_category_posts_admin import (
    GetCategoryPostsAdminUseCase,
)
from application.domain.category.use_cases.update_category import (
    UpdateCategoryUseCase,
)
from application.domain.comment.use_cases.create_comment import (
    CreateCommentUseCase,
)
from application.domain.comment.use_cases.create_comment_admin import (
    CreateCommentAdminUseCase,
)
from application.domain.comment.use_cases.delete_comment import (
    DeleteCommentUseCase,
)
from application.domain.comment.use_cases.delete_comment_admin import (
    DeleteCommentAdminUseCase,
)
from application.domain.comment.use_cases.get_comment import (
    GetCommentUseCase,
)
from application.domain.comment.use_cases.get_comment_admin import (
    GetCommentAdminUseCase,
)
from application.domain.comment.use_cases.update_comment import (
    UpdateCommentUseCase,
)
from application.domain.comment.use_cases.update_comment_admin import (
    UpdateCommentAdminUseCase,
)
from application.domain.location.use_cases.create_location import (
    CreateLocationUseCase,
)
from application.domain.location.use_cases.delete_location import (
    DeleteLocationUseCase,
)
from application.domain.location.use_cases.get_location import (
    GetLocationUseCase,
)
from application.domain.location.use_cases.get_location_admin import (
    GetLocationAdminUseCase,
)
from application.domain.location.use_cases.get_location_posts import (
    GetLocationPostsUseCase,
)
from application.domain.location.use_cases.get_location_posts_admin import (
    GetLocationPostsAdminUseCase,
)
from application.domain.location.use_cases.update_location import (
    UpdateLocationUseCase,
)
from application.domain.post.use_cases.add_post_image import AddPostImageUseCase
from application.domain.post.use_cases.create_post import CreatePostUseCase
from application.domain.post.use_cases.create_post_admin import (
    CreatePostAdminUseCase,
)
from application.domain.post.use_cases.delete_post import DeletePostUseCase
from application.domain.post.use_cases.delete_post_admin import (
    DeletePostAdminUseCase,
)
from application.domain.post.use_cases.get_post import GetPostUseCase
from application.domain.post.use_cases.get_post_admin import GetPostAdminUseCase
from application.domain.post.use_cases.get_post_comments import (
    GetPostCommentsUseCase,
)
from application.domain.post.use_cases.get_post_comments_admin import (
    GetPostCommentsAdminUseCase,
)
from application.domain.post.use_cases.get_post_image import GetPostImageUseCase
from application.domain.post.use_cases.get_posts_last_list import (
    GetPostsLastListUseCase,
)
from application.domain.post.use_cases.update_post import UpdatePostUseCase
from application.domain.post.use_cases.update_post_admin import (
    UpdatePostAdminUseCase,
)
from application.domain.user.use_cases.create_user import CreateUserUseCase
from application.domain.user.use_cases.create_user_admin import (
    CreateUserAdminUseCase,
)
from application.domain.user.use_cases.delete_user_by_username import (
    DeleteUserByUsernameUseCase,
)
from application.domain.user.use_cases.get_user_by_username import (
    GetUserByUsernameUseCase,
)
from application.domain.user.use_cases.get_user_by_username_admin import (
    GetUserByUsernameAdminUseCase,
)
from application.domain.user.use_cases.get_user_posts_by_username import (
    GetUserPostsByUsernameUseCase,
)
from application.domain.user.use_cases.get_user_posts_by_username_admin import (
    GetUserPostsByUsernameAdminUseCase,
)
from application.domain.user.use_cases.update_user_by_username import (
    UpdateUserByUsernameUseCase,
)
from application.domain.user.use_cases.update_user_by_username_admin import (
    UpdateUserByUsernameAdminUseCase,
)


def authenticate_user_use_case() -> AuthenticateUserUseCase:
    return AuthenticateUserUseCase()


def create_access_token_use_case() -> CreateAccessTokenUseCase:
    return CreateAccessTokenUseCase()


def get_user_by_username_use_case() -> GetUserByUsernameUseCase:
    return GetUserByUsernameUseCase()


def get_user_posts_by_username_use_case() -> GetUserPostsByUsernameUseCase:
    return GetUserPostsByUsernameUseCase()


def create_user_use_case() -> CreateUserUseCase:
    return CreateUserUseCase()


def update_user_by_username_use_case() -> UpdateUserByUsernameUseCase:
    return UpdateUserByUsernameUseCase()


def delete_user_by_username_use_case() -> DeleteUserByUsernameUseCase:
    return DeleteUserByUsernameUseCase()


def get_user_by_username_admin_use_case() -> GetUserByUsernameAdminUseCase:
    return GetUserByUsernameAdminUseCase()


def create_user_admin_use_case() -> CreateUserAdminUseCase:
    return CreateUserAdminUseCase()


def get_user_posts_by_username_admin_use_case() -> (
    GetUserPostsByUsernameAdminUseCase
):
    return GetUserPostsByUsernameAdminUseCase()


def update_user_by_username_admin_use_case() -> (
    UpdateUserByUsernameAdminUseCase
):
    return UpdateUserByUsernameAdminUseCase()


def get_post_use_case() -> GetPostUseCase:
    return GetPostUseCase()


def get_post_comments_use_case() -> GetPostCommentsUseCase:
    return GetPostCommentsUseCase()


def get_posts_last_list_use_case() -> GetPostsLastListUseCase:
    return GetPostsLastListUseCase()


def create_post_use_case() -> CreatePostUseCase:
    return CreatePostUseCase()


def update_post_use_case() -> UpdatePostUseCase:
    return UpdatePostUseCase()


def delete_post_use_case() -> DeletePostUseCase:
    return DeletePostUseCase()


def add_post_image_use_case() -> AddPostImageUseCase:
    return AddPostImageUseCase()


def get_post_image_use_case() -> GetPostImageUseCase:
    return GetPostImageUseCase()


def get_post_admin_use_case() -> GetPostAdminUseCase:
    return GetPostAdminUseCase()


def get_post_comments_admin_use_case() -> GetPostCommentsAdminUseCase:
    return GetPostCommentsAdminUseCase()


def create_post_admin_use_case() -> CreatePostAdminUseCase:
    return CreatePostAdminUseCase()


def update_post_admin_use_case() -> UpdatePostAdminUseCase:
    return UpdatePostAdminUseCase()


def delete_post_admin_use_case() -> DeletePostAdminUseCase:
    return DeletePostAdminUseCase()


def get_comment_use_case() -> GetCommentUseCase:
    return GetCommentUseCase()


def create_comment_use_case() -> CreateCommentUseCase:
    return CreateCommentUseCase()


def update_comment_use_case() -> UpdateCommentUseCase:
    return UpdateCommentUseCase()


def delete_comment_use_case() -> DeleteCommentUseCase:
    return DeleteCommentUseCase()


def get_comment_admin_use_case() -> GetCommentAdminUseCase:
    return GetCommentAdminUseCase()


def create_comment_admin_use_case() -> CreateCommentAdminUseCase:
    return CreateCommentAdminUseCase()


def update_comment_admin_use_case() -> UpdateCommentAdminUseCase:
    return UpdateCommentAdminUseCase()


def delete_comment_admin_use_case() -> DeleteCommentAdminUseCase:
    return DeleteCommentAdminUseCase()


def get_category_use_case() -> GetCategoryUseCase:
    return GetCategoryUseCase()


def get_category_posts_use_case() -> GetCategoryPostsUseCase:
    return GetCategoryPostsUseCase()


def create_category_use_case() -> CreateCategoryUseCase:
    return CreateCategoryUseCase()


def update_category_use_case() -> UpdateCategoryUseCase:
    return UpdateCategoryUseCase()


def delete_category_use_case() -> DeleteCategoryUseCase:
    return DeleteCategoryUseCase()


def get_category_admin_use_case() -> GetCategoryAdminUseCase:
    return GetCategoryAdminUseCase()


def get_category_posts_admin_use_case() -> GetCategoryPostsAdminUseCase:
    return GetCategoryPostsAdminUseCase()


def get_location_use_case() -> GetLocationUseCase:
    return GetLocationUseCase()


def get_location_posts_use_case() -> GetLocationPostsUseCase:
    return GetLocationPostsUseCase()


def create_location_use_case() -> CreateLocationUseCase:
    return CreateLocationUseCase()


def update_location_use_case() -> UpdateLocationUseCase:
    return UpdateLocationUseCase()


def delete_location_use_case() -> DeleteLocationUseCase:
    return DeleteLocationUseCase()


def get_location_admin_use_case() -> GetLocationAdminUseCase:
    return GetLocationAdminUseCase()


def get_location_posts_admin_use_case() -> GetLocationPostsAdminUseCase:
    return GetLocationPostsAdminUseCase()
