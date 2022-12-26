import feedparser

from textual.app import App, ComposeResult
from textual.containers import Container
from textual.widgets import Static, Header, Footer

blog_rss_url = "https://meetgor.com/rss"
feeds = feedparser.parse(blog_rss_url)
posts = []
for post in feeds.entries:
    post["title"] = post.title
    post["description"] = post.summary
    post["link"] = post.link
    posts.append(post)


class BlogTUI(App):
    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield Footer()
        yield Container(id="blog_container")

    def on_mount(self) -> None:
        blog_container = self.query_one("#blog_container")
        for post in posts:
            title = Static(f"{post['title']}")
            description = Static(f"{post['description']}")
            blog_container.mount(title, description)
            title.styles.border = ("heavy", "white")


def main():
    app = BlogTUI()
    app.run()


if __name__ == "__main__":
    main()
