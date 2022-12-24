import os
import json
from json import JSONEncoder

ALLOWABLE_IMAGE_TYPES = [
    "jpg", "jpeg", "png"
]


class Folder:

    def __init__(self, path_to_folder):

        self.path = path_to_folder

        self._score_file_location = os.path.join(self.path, "scores.json")

        # if the scores file already exists, load it!
        if os.path.exists(self._score_file_location):
            with open(self._score_file_location, "r") as state_file:

                self.images = [ScoredImage(o['path'], o['score']) for o in json.load(state_file)]

        else:
            self.images = [ScoredImage(os.path.join(self.path, path_to_image)) for path_to_image in os.listdir(self.path) \
                           if path_to_image.split('.')[-1].lower() in ALLOWABLE_IMAGE_TYPES ]
            print(self.images)

    def save(self):

        with open(self._score_file_location, "w") as state_file:
            simple_objects = [{"path": o.path,
                               "score": o.score} for o in self.images]
            state_file.write(json.dumps(simple_objects))

    def __repr__(self):
        return str(self.images)

    def __iter__(self):
        # iterator to make the class able to be able to be used in loops etc.
        i = 0
        while i < len(self.images):
            yield self.images[i]
            i += 1


class ScoredImage:

    def __init__(self, path_to, score: int = 0):
        self.path = path_to
        self.score = score

    def __repr__(self):
        return str((self.path, self.score))


if __name__ == "__main__":
    folder = Folder("/home/patrickpragman/PycharmProjects/label_maker/panes/images")
    print(folder)
    for o in folder:
        o.score += 1


    folder.save()
