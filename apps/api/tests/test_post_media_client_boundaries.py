"""Negative A/B/C post and media tests using only synthetic records.

These tests describe existing BrightBean behavior. In particular, an
organization-wide shared media asset remains visible across workspaces:
that is a product-design risk for VIGIAFAST private evidence, not approval
to store evidence in the shared media library.
"""

from __future__ import annotations

import json

import pytest

from apps.api.tests.test_cross_client_isolation import (
    _SecureClient,
    _call_mcp,
    clients,
)
from apps.api_keys import services
from apps.composer.models import PlatformPost, Post
from apps.media_library.models import MediaAsset


@pytest.fixture
def scoped_posts(clients):
    posts = []
    for index, workspace in enumerate(clients.workspaces):
        post = Post.objects.create(
            workspace=workspace,
            caption=f"confidential-caption-{index}",
            internal_notes=f"private-note-{index}",
        )
        PlatformPost.objects.create(
            post=post,
            social_account=clients.accounts[index],
        )
        posts.append(post)
    return tuple(posts)


@pytest.fixture
def scoped_media(clients):
    workspaces = clients.workspaces
    entries = [
        (workspaces[0], workspaces[0].organization, "client-a.png"),
        (workspaces[1], workspaces[1].organization, "client-b.png"),
        (workspaces[2], workspaces[2].organization, "client-c.png"),
        (None, workspaces[0].organization, "agency-shared.png"),
        (None, workspaces[2].organization, "other-org-shared.png"),
    ]
    assets = []
    for index, (workspace, organization, name) in enumerate(entries):
        asset = MediaAsset.objects.create(
            organization=organization,
            workspace=workspace,
            filename=name,
            file=f"media_library/synthetic/{index}.png",
            media_type=MediaAsset.MediaType.IMAGE,
            mime_type="image/png",
            processing_status=MediaAsset.ProcessingStatus.COMPLETED,
        )
        assets.append(asset)
    return tuple(assets)


@pytest.fixture
def writer_client(clients):
    key = services.issue_api_key(
        workspace=clients.workspaces[0],
        social_accounts=[clients.accounts[0]],
        issued_by=clients.user,
        name="synthetic-post-writer",
        permissions=["create_posts"],
    )
    return _SecureClient(
        HTTP_AUTHORIZATION=f"Bearer {key.plaintext_token}"
    )


@pytest.mark.django_db
class TestPostAndMediaBoundaries:
    def test_rest_reads_own_post(self, clients, scoped_posts):
        response = clients.rest.get(
            f"/api/v1/posts/{scoped_posts[0].id}"
        )
        assert response.status_code == 200, response.content
        assert response.json()["id"] == str(scoped_posts[0].id)

    @pytest.mark.parametrize("other_idx", [1, 2])
    def test_rest_cannot_read_other_client_post(
        self, clients, scoped_posts, other_idx
    ):
        response = clients.rest.get(
            f"/api/v1/posts/{scoped_posts[other_idx].id}"
        )
        assert response.status_code == 404
        assert f"confidential-caption-{other_idx}" not in (
            response.content.decode()
        )

    @pytest.mark.parametrize("other_idx", [1, 2])
    def test_mcp_cannot_read_other_client_post(
        self, clients, scoped_posts, other_idx
    ):
        response = _call_mcp(
            clients.rest,
            "get_post",
            {"post_id": str(scoped_posts[other_idx].id)},
        )
        data = response.json()
        assert "error" in data, data
        assert f"private-note-{other_idx}" not in response.content.decode()

    @pytest.mark.parametrize("other_idx", [1, 2])
    def test_rest_cannot_edit_other_client_post(
        self, writer_client, scoped_posts, other_idx
    ):
        original = scoped_posts[other_idx].caption
        response = writer_client.patch(
            f"/api/v1/posts/{scoped_posts[other_idx].id}",
            data=json.dumps({"caption": "unauthorized replacement"}),
            content_type="application/json",
        )
        assert response.status_code == 404, response.content
        scoped_posts[other_idx].refresh_from_db()
        assert scoped_posts[other_idx].caption == original

    def test_rest_media_list_excludes_other_clients_and_org(
        self, clients, scoped_media
    ):
        response = clients.rest.get("/api/v1/media/")
        assert response.status_code == 200, response.content
        filenames = {item["filename"] for item in response.json()["items"]}
        assert filenames == {"client-a.png", "agency-shared.png"}

    def test_mcp_media_search_has_same_scope(self, clients, scoped_media):
        response = _call_mcp(clients.rest, "search_media", {})
        data = response.json()
        assert "result" in data, data
        body = json.loads(data["result"]["content"][0]["text"])
        filenames = {item["filename"] for item in body["items"]}
        assert filenames == {"client-a.png", "agency-shared.png"}

    @pytest.mark.parametrize("other_idx", [1, 2, 4])
    def test_rest_denies_direct_foreign_media_uuid(
        self, clients, scoped_media, other_idx
    ):
        response = clients.rest.get(
            f"/api/v1/media/{scoped_media[other_idx].id}"
        )
        assert response.status_code == 404

    @pytest.mark.parametrize("other_idx", [1, 2, 4])
    def test_mcp_denies_direct_foreign_media_uuid(
        self, clients, scoped_media, other_idx
    ):
        response = _call_mcp(
            clients.rest,
            "get_media",
            {"media_id": str(scoped_media[other_idx].id)},
        )
        data = response.json()
        assert "error" in data, data

    def test_org_shared_media_is_visible_inside_same_org(
        self, clients, scoped_media
    ):
        """Existing capability, NOT permission for private evidence."""
        response = clients.rest.get(
            f"/api/v1/media/{scoped_media[3].id}"
        )
        assert response.status_code == 200, response.content
        assert response.json()["is_shared"] is True
        assert response.json()["workspace_id"] is None
