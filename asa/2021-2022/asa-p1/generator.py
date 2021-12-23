import random
import argparse
import subprocess

parser = argparse.ArgumentParser(description='Generate random sequences to test ASA\'s 1st project 2021-2022')
parser.add_argument('file', metavar='file_name', type=str, help='the name of the executable to run (your program)')
parser.add_argument('--seed', '-s', default=20211223, dest='seed', type=int, help='[Advanced] The seed of the random number generator. The same seed always produces the same input numbers (default is 20211223).')
parser.add_argument('--sequence-length', '-l', default=10000, dest='seq_length', type=int, help='The length of the sequences to generate (default is 10 000).')
parser.add_argument('--max-num', '-n', default=10000, dest='max_num', type=int, help='The max number to include in the sequences (default is 10 000).')
parser.add_argument('--test-count', '-t', default=1000, dest='test_count', type=int, help='How many tests to run (default is 1 000).')
parser.add_argument('--quiet', '-q', dest='quiet', action='store_true', help='Toggle to disable verbose output and print only the program output.')

args = parser.parse_args()

random.seed(args.seed)

for run in range(args.test_count):
  if not args.quiet:
    print(f"--- Test run {run + 1} ---")

  test_input = "1\n"
  nums = []
  for _ in range(args.seq_length):
    nums.append(str(random.randint(1, args.max_num)));

  test_input = f"{test_input}{' '.join(nums)}\n"

  result = subprocess.run([args.file], input=test_input.encode('utf-8'), capture_output=True)

  if result.returncode != 0:
    print(f"Program exited with errorcode {result.returncode}. Aborting tests")
    break

  print(result.stdout.decode().strip())
