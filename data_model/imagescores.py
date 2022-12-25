import os
import json
from json import JSONEncoder

ALLOWABLE_IMAGE_TYPES = [
    "jpg", "jpeg", "png"
]

ALLOWABLE_SCORES = [
    -1, 0, 1, 2, 3
]


class Folder:

    def __init__(self, path_to_folder):

        self.path = path_to_folder

        self._score_file_location = os.path.join(self.path, "scores.json")

        # if the scores file already exists, load it!
        if os.path.exists(self._score_file_location):
            with open(self._score_file_location, "r") as state_file:

                json_dict = json.load(state_file)

                self.images = [ScoredImage(o['path'], o['score']) for o in json_dict['images']]
                path = json_dict['last_image']

                images = [image for image in self.images if image.path == path]
                self.current_image = images[0] if images else None

        else:
            self.images = [ScoredImage(os.path.join(self.path, path_to_image)) for path_to_image in
                           os.listdir(self.path) \
                           if path_to_image.split('.')[-1].lower() in ALLOWABLE_IMAGE_TYPES]

            self.current_image = self.images[0] if self.images else None

    def save(self):

        with open(self._score_file_location, "w") as state_file:
            simple_objects = {"images": [{"path": o.path,
                                          "score": o.score} for o in self.images],
                              "last_image": self.current_image.path if isinstance(self.current_image, ScoredImage) else None}
            state_file.write(json.dumps(simple_objects))

    def __repr__(self):
        return str(self.images)

    def __str__(self):
        return self.path

    def __iter__(self):
        # iterator to make the class able to be able to be used in loops etc.
        i = 0
        while i < len(self.images):
            yield self.images[i]
            i += 1


class ScoredImage:

    def __init__(self, path_to, score: int = -1):
        self.path = path_to
        self._score = score

    """
    using properties because I may want to add functionality here later
    """

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, value):
        if value not in ALLOWABLE_SCORES:
            msg = """you're trying to set the value of an
ScoreImage object to something other than one of the 
allowable scores - that is something other than -1, 0, 2, or 3.
No other scores are allowable."""
            raise Exception(msg)
        else:
            self._score = value

    def force_score(self, value):
        self.score = value

    def __repr__(self):
        return str((self.path, self._score))

    def __str__(self):
        return self.path

    def __eq__(self, other):
        return self.path == other.path


if __name__ == "__main__":
    folder = Folder("/home/patrickpragman/PycharmProjects/label_maker/panes/images")
    print(folder)
    for o in folder:
        o.score += 1

    folder.save()
