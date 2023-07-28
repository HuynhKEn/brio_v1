import os
import sys
import struct
import hashlib
import argparse
import subprocess
import collections


dm_single_close_quote = u'\u2019'
dm_double_close_quote = u'\u201d'
END_TOKENS = ['.', '!', '?', '...', "'", "`", '"', dm_single_close_quote, dm_double_close_quote, ")"] # acceptable ways to end a sentence


def read_text_file(text_file):
  lines = []
  with open(text_file, "r", encoding="utf-8") as f:
    for line in f:
      lines.append(line.strip())
  return lines


def hashhex(s):
  """Returns a heximal formated SHA1 hash of the input string."""
  h = hashlib.sha1()
  h.update(s.encode())
  return h.hexdigest()


def get_url_hashes(url_list):
  return [hashhex(url) for url in url_list]


def fix_missing_period(line):
  """Adds a period to a line that is missing a period"""
  if '@highlight' in line: return line
  if line=="": return line
  if line[-1] in END_TOKENS: return line
  return line + " ."


def get_art_abs(story_file):
  lines = read_text_file(story_file)

  # Put periods on the ends of lines that are missing them (this is a problem in the dataset because many image captions don't end in periods; consequently they end up in the body of the article as run-on sentences)
  lines = [fix_missing_period(line) for line in lines]

  # Separate out article and abstract sentences
  article_lines = []
  highlights = []
  next_is_highlight = False
  for idx,line in enumerate(lines):
    if line == "":
      continue # empty line
    elif line.startswith("@highlight"):
      next_is_highlight = True
    elif next_is_highlight:
      highlights.append(line)
    else:
      article_lines.append(line)

  # Make article into a single string
  article = ' '.join(article_lines)

  # Make abstract into a signle string
  abstract = ' '.join(highlights)

  return article, abstract


def write_to_bin(dir_path, out_prefix):
  count=0
  """Reads the .story files corresponding to the urls listed in the url_file and writes them to a out_file."""

  print("Making bin file for URLs listed in %s..." % dir_path)

  story_fnames = os.listdir(dir_path)
  with open(out_prefix + '.source', 'wt', encoding="utf-8") as source_file, open(out_prefix + '.target', 'wt',encoding="utf-8") as target_file:
    for idx,s in enumerate(story_fnames):
      print(s)
      # Look in the story dirs to find the .story file corresponding to this ur
      count=count+1
      if os.path.isfile(os.path.join(dir_path, s)):
        print(count)
        story_file = os.path.join(dir_path, s)
      else:
        print("Error: Couldn't find story file %s in either story directories %s and %s." % (s, dir_path))

      # Get the strings to write to .bin file
      article, abstract = get_art_abs(story_file)

      # Write article and abstract to files
      if article.strip() not in "":
        source_file.write(article.replace("VOV.VN -", "").replace("- ", "").strip() + '\n')
        target_file.write(abstract.replace("VOV.VN -", "").replace("- ", "").strip() + '\n')

  print("Finished writing files")


def check_num_stories(stories_dir, num_expected):
  num_stories = len(os.listdir(stories_dir))
  if num_stories != num_expected:
    raise Exception("stories directory %s contains %i files but should contain %i" % (stories_dir, num_stories, num_expected))


def run(type_document, source_dir = "", des_src = ""):
  """
    This function split total raw data to train, val, test
    
    Parameters:
    source_dir (str): dir of list storie files.
    des_src (str): dir of output file.    
  """
  if not os.path.exists(des_src):
    os.makedirs(des_src)
  print("start create bin:", type_document)
  write_to_bin(source_dir, os.path.join(des_src, type_document))
