import graphene
from graphene_django import DjangoObjectType
from blog.models import Post, Comment
from graphql import GraphQLError


class PostType(DjangoObjectType):
    class Meta:
        model = Post


class CommentType(DjangoObjectType):
    class Meta:
        model = Comment


class Query(graphene.ObjectType):
    """ Main Query for Fetching Post related data"""

    posts = graphene.List(PostType)
    post = graphene.Field(PostType, post_id=graphene.Int(required=True))

    def resolve_posts(self, info):
        """Returns list of posts"""
        return Post.objects.all()

    def resolve_post(self, info, post_id):
        """
        Get details about a single post based on post_id
        """
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            raise GraphQLError("Blog does not exist")
        return post


class CreatePost(graphene.Mutation):
    '''Mutation to create a new post'''

    post = graphene.Field(PostType)

    class Arguments:
        title = graphene.String()
        description = graphene.String()
        author = graphene.String()

    def mutate(self, info, title, description, author):
        post = Post.objects.create(
            title=title, description=description, author=author
        )
        return CreatePost(post=post)


class UpdatePost(graphene.Mutation):
    """Mutation to update an existing post based on post id"""
    post = graphene.Field(PostType)

    class Arguments:
        post_id = graphene.Int(required=True)
        title = graphene.String()
        description = graphene.String()

    def mutate(self, info, post_id, title, description):
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            raise GraphQLError('Cannot update post which does not exist')

        post.title = title
        post.description = description
        post.save()
        return UpdatePost(post=post)


class CreateComment(graphene.Mutation):
    """Mutation to create a new comment on a post"""

    comment = graphene.Field(CommentType)

    class Arguments:
        post_id = graphene.Int()
        text = graphene.String()
        author = graphene.String()

    def mutate(self, info, post_id, text, author):
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            raise GraphQLError(
                "Cannot comment on a post which does not exist!")
        comment = Comment.objects.create(
            post=post, text=text, author=author
        )
        comment.save()
        return CreateComment(comment=comment)


class DeleteComment(graphene.Mutation):
    """Mutation to delete an existing comment based on comment id"""

    id = graphene.Int()

    class Arguments:
        id = graphene.Int(required=True)

    def mutate(self, info, id):
        try:
            comment = Comment.objects.get(id=id)
        except Comment.DoesNotExist:
            raise GraphQLError('Cannot delete comment which does not exist')
        comment.delete()
        return DeleteComment(id=id)


class Mutation(graphene.ObjectType):
    create_post = CreatePost.Field()
    update_post = UpdatePost.Field()
    create_comment = CreateComment.Field()
    delete_comment = DeleteComment.Field()
