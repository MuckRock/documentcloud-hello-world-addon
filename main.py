"""
This is a hello world add-on for DocumentCloud.

It demonstrates how to write a add-on which can be activated from the
DocumentCloud add-on system and run using Github Actions.  It receives data
from DocumentCloud via the request dispatch and writes data back to
DocumentCloud using the standard API
"""

from documentcloud.addon import AddOn


class HelloWorld(AddOn):
    """An example Add-On for DocumentCloud."""

    def main(self):
        """The main add-on functionality goes here."""
        # fetch your add-on specific data
        name = self.data.get("name", "world")

        self.set_message("Hello World start!")

        # add a hello note to the first page of each selected document
        for document in self.get_documents():
            # get_documents will iterate through all documents efficiently,
            # either selected or by query, dependeing on which is passed in
            document.annotations.create(f"Hello {name}!", 0)

        with open("hello.txt", "w+") as file_:
            file_.write("Hello world!")
            self.upload_file(file_)

        self.set_message("Hello World end!")
        self.send_mail("Hello World!", "We finished!")


if __name__ == "__main__":
    HelloWorld().main()
