from textual.app import App, ComposeResult
from textual.containers import Container
from textual.widgets import Static, Header, Footer, Button
import docker



class DockerTUI(App):
    def compose(self) -> ComposeResult:
        yield Header()
        yield Container(id="dcontainers")
        yield Footer()

    def get_all_containers(self) -> None:
        containers = self.query_one("#dcontainers")
        client = docker.from_env()
        docker_containers = [docker for docker in client.containers.list()]
        for container in docker_containers:
            docker_container = Container(
                    Static(f"{container.name}"),
                    Button("Start"),
                    Button("Stop", id=f"{container.name}_stop"),
                    id=f"container_{container.name}",
                    )
            docker_container.styles.border = ("heavy", "white")
            self.query_one("#dcontainers").refresh()
        client.close()


    def on_mount(self) -> None:
        containers = self.query_one("#dcontainers")
        client = docker.from_env()
        docker_containers = [docker for docker in client.containers.list(all=True)]
        for container in docker_containers:
            if container.status != "running":
                docker_container = Container(
                        Static(f"{container.name}"),
                        Button("Start"),
                        Button("Stop", id=f"{container.name}_stop"),
                        id=f"container_{container.name}",
                        )
                docker_container.styles.border = ("heavy", "white")
                docker_container.styles.height= "10" 
                containers.mount(docker_container)
        client.close()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        button_id = event.button.id
        if button_id.split("_")[-1] == "stop":
            container_name = button_id.split("_")[0]
            client = docker.from_env()
            container = client.containers.get(container_name)
            container.stop()
            self.query_one(f"#container_{container_name}").remove()
            self.get_all_containers()
            client.close()


def main():
    app = DockerTUI()
    app.run()


if __name__ == "__main__":
    main()
