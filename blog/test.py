from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Post
from taggit.models import Tag

class PostTagTestCase(TestCase):
    def setUp(self):
        # ✅ Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass'
        )

        # ✅ Create a post with an author assigned
        self.post = Post.objects.create(
            title="Test Post",
            slug="test-post",
            body="This is a test post.",
            status="published",
            author=self.user  # ← THIS IS REQUIRED AND MISSING IN YOUR FAILING TEST
        )

        self.post.tags.add("django", "very-long-tag-name-that-exceeds-25-characters")

    def test_post_creation(self):
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(self.post.title, "Test Post")

    def test_tags_assigned(self):
        self.assertEqual(self.post.tags.count(), 2)
        self.assertIn("django", [tag.name for tag in self.post.tags.all()])

    def test_tag_slug_length(self):
        tag = Tag.objects.get(name="very-long-tag-name-that-exceeds-25-characters")
        self.assertTrue(len(tag.slug) > 25)
        self.assertLessEqual(len(tag.slug), 100)

    def test_tag_url_resolves(self):
        response = self.client.get(reverse("blog:post_list_by_tag", args=["django"]))
        self.assertEqual(response.status_code, 200)
