#!/usr/bin/python3

import csv
import json
import os
from collections import OrderedDict
import sys
import ntpath


class EventJsonToCsv:
    """Converts event data provided by Facebook's Graph API into CSV format"""

    RELEVANT_KEYS = ['id', 'name', 'startTime', 'endTime', 'distance']
    METADATA_KEYS = ['venues','venuesWithEvents','events']

    def strip_file(self, source):
        """Removes the path and file extension from a given filepath

        :param source: The path of the file
        :return: The filename without any path info or file extension
        """
        head, tail = ntpath.split(source)

        def remove_ending(file):
            return os.path.splitext(file)[0]

        return remove_ending(tail) or remove_ending(ntpath.basename(head))

    def json_to_csv(self, source):
        """Does the actual conversion

        Takes a .json file, which is specified by path, and converts it
        into csv format.
        A new file in csv format is created in the outputs
        folder with the same filename as the sourcefile.
        Only the keys contained in RELEVANT_KEYS and the Metada is converted.
        :param source: The path of the file, which should be converted
        :return: None
        """
        with open(source) as data_file:
            data = json.load(data_file, encoding='utf-8',
                             object_pairs_hook=OrderedDict)
            events = []
            metadata = data['metadata']
            for event in data['events']:
                events.append(event)

            output_dir = 'outputs'
            if not os.path.isdir(output_dir):
                os.mkdir(output_dir)
            filename = self.strip_file(source)+'.csv'

            with open(os.path.join(output_dir, filename), 'w', newline='') as output_file:
                csvWriter = csv.writer(output_file, quoting=csv.QUOTE_MINIMAL)
                csvWriter.writerow(self.RELEVANT_KEYS)
                for event in events:
                    csvWriter.writerow([event[key] for key in self.RELEVANT_KEYS])
                csvWriter.writerow(self.METADATA_KEYS)
                csvWriter.writerow([metadata[key] for key in self.METADATA_KEYS])


if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise IOError('Number of arguments is faulty, specify exactly one '
                      'argument containing either a folder or a file as input')
    else:
        jtc = EventJsonToCsv()
        source = sys.argv[1]
        if os.path.isfile(source):
            jtc.json_to_csv(source)
        elif os.path.isdir(source):
            for __, __, files in os.walk(source):
                for file in files:
                    if file.endswith('.json'):
                        jtc.json_to_csv(os.path.join(source, file))
                    else:
                        continue
        else:
            raise IOError('The given argument is neither a file nor a directory')
