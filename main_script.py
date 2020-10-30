import argparse
from p_acquisition import m_acquisition as mac
from p_wrangling import m_wrangling as mwr
from p_analysis import m_analysis as man


def argument_parser():
    choices_list = ['Y', 'N']
    parser = argparse.ArgumentParser(description='Set conditions to the program')
    parser.add_argument("-s", "--scraping", type=str, choices=choices_list, dest='scrape',
                        default='N', help="Scrape and update the beer database")
    parser.add_argument("-d", "--download", type=str, choices=choices_list, dest='download',
                        default='N', help="Download the beers of the supermarkets")
    parser.add_argument("-m", "--model", type=str, choices=choices_list, dest='model',
                        default='N', help="Fit the model with new images")

    args = parser.parse_args()
    return args


def main(scrape, download, model):
    print('Starting Pipeline...')
    mac.acquire(scrape)
    mwr.wrangle(scrape, download)
    man.analyze(model)
    print('Finished Pipeline')


if __name__ == '__main__':
    arguments = argument_parser()
    main(arguments.scrape, arguments.download, arguments.model)
