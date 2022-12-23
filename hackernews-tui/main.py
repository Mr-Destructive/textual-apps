import requests
import json

from textual.app import App, ComposeResult
from textual.containers import Container
from textual.widgets import Static, Header, Footer

hacker_news_popular_url = "https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty"
post_ids = requests.get(hacker_news_popular_url)
post_ids = json.loads(post_ids.content)[:10]



class HackerNewsTUI(App):
    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield Footer()
        yield Container(id="hn_container")

    def on_mount(self) -> None:
        hn_container = self.query_one("#hn_container")
        for post_id in post_ids:
            hacker_news_post_url = f"https://hacker-news.firebaseio.com/v0/item/{post_id}.json?print=pretty"
            post_data = requests.get(hacker_news_post_url)
            post_data = json.loads(post_data.content)
            if "url" in post_data:
                print(post_data["url"])
                post = Static(f"[link={post_data['url']}]{post_data['title']}[/]")
                post.styles.border = ("heavy", "white")
                hn_container.mount(post)


def main():
    app = HackerNewsTUI()
    app.run()


if __name__ == "__main__":
    main()
