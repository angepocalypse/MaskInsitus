class ArtData:
    ASPECT_RATIOS = [(2, 3), (3, 4), (4, 5), (5, 7), (11, 14)]

    '''
    Class for handling all of the image and metadata for a piece of art
    '''
    def __init__(self, title: str, url: str, thumb_url: str, dimensions: list):
        self.title = title
        self.url = url
        self.thumb_url = thumb_url
        self.dimensions = dimensions
        self.width = dimensions[0]
        self.height = dimensions[1]

    def show(self):
        print("Title:", self.title)
        print("Image URL:", self.url)
        print("Image Size: {} x {}".format(self.dimensions[0], self.dimensions[1]))

    def get_closest_aspect_ratio(self):
        target_ratio = self.width / self.height if self.is_portrait() else self.height / self.width
        closest_ratio = None
        min_difference = float('inf')

        for ratio in self.ASPECT_RATIOS:
            aspect_ratio = ratio[0] / ratio[1]
            difference = abs(aspect_ratio - target_ratio)

            if difference < min_difference:
                min_difference = difference
                closest_ratio = ratio

        return closest_ratio

    def is_portrait(self):
        return self.height > self.width

