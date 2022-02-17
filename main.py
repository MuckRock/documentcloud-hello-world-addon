"""
This is a hello world plugin for DocumentCloud.

It demonstrates how to write a plugin which can be activated from the
DocumentCloud plugin system and run using Github Actions.  It receives data
from DocumentCloud via the request dispatch and writes data back to
DocumentCloud using the standard API
"""

from addon import AddOn


class HelloWorld(AddOn):
    """An example Add-On for DocumentCloud."""

    def main(self):
        """The main plugin functionality goes here."""
        # fetch your plugin specific data
        name = self.data.get("name", "world")

        self.set_message("Hello World start!")

        # add a hello note to the first page of each selected document
        if self.documents:
            length = len(self.documents)
            for i, doc_id in enumerate(self.documents):
                self.set_progress(100 * i // length)
                document = self.client.documents.get(doc_id)
                document.annotations.create(f"Hello {name}!", 0)
        elif self.query:
            documents = self.client.documents.search(self.query)
            length = len(documents)
            for i, document in enumerate(documents):
                self.set_progress(100 * i // length)
                document.annotations.create(f"Hello {name}!", 0)

        with open("hello.txt", "w+") as file_:
            file_.write("Hello world!")
            self.upload_file(file_)

        self.set_message("Hello World end!")


if __name__ == "__main__":
    HelloWorld().main()
