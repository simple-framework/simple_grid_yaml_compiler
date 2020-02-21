class Part:
    def __init__(self, filename, starting_line):
        self.filename = filename
        self.starting_line_number = -1
        self.starting_line = starting_line
        self.num_of_lines = 0

    def find_line(self, input_text_file):
        with open(input_text_file, 'r') as f:
            for index, line in enumerate(f.readlines()):
                if line == "{flag}\n".format(flag=self.starting_line):
                    self.starting_line_number = index
                    break


class Tracker:
    parts = []

    @staticmethod
    def create_part(filename, starting_line):
        Tracker.parts.append(Part(filename, starting_line))

    @staticmethod
    def reorder_parts(filename):
        for part in Tracker.parts:
            part.find_line(filename)


if __name__ == "__main__":
    Tracker.create_part("site repo defaults", "default_vo_generic_dn_ca_cern: &default_vo_generic_dn_ca_cern '/DC=ch/DC=cern/CN=CERN Grid Certification Authority'")

    Tracker.reorder_parts('./.temp/runtime.yaml')

    print(Tracker.parts[0].starting_line_number)

    print("End")