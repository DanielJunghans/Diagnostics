# Will go thourgh each directory and see if the folder exists and count the
# number of finsihed runs.
#
# Input:
#   arg1 -> Directory where the data is located
#   arg2 -> What selection scheme are we checking
#   arg3 -> What generation are we checking
#
# Output : print out the seeds that are not finished running for a treatment replicate
#
# python3

# Imports
import datetime
import argparse
import os
import pandas as pd

# VARIABLES EVERYONE NEEDS TO KNOW
REPLICATION_OFFSET=0
DATA_DIR='/mnt/scratch/junghan2/Diagnostics/Data/'
POP_FILE = "/Unique_Genomes_Pop.csv"
REPLICATES = 100
NOW = datetime.datetime.now()


######################## LEXICASE ########################
LEX_POP_SIZE = [10, 100, 500, 700, 1000]
LEX_OFFSET = 0
LEX_DIR_1 = "SEL_LEXICASE__DIA_Exploitation__POP_"
LEX_DIR_2 = "__TRT_100__SEED_"

def lex(d_dir, GENRATIONS):
  print('-----------------------------'*4)
  print('Processing Lexicase Runs-' + str(NOW))

  lost = []

  for i in range(len(LEX_POP_SIZE)):
    for r in range(1,REPLICATES+1):
      # Create the directory
      seed = (r + (i * 100)) + LEX_OFFSET + REPLICATION_OFFSET
      dir = d_dir + LEX_DIR_1 + str(LEX_POP_SIZE[i]) + LEX_DIR_2 + str(seed)

      # Check to see if directory exists
      if(os.path.isdir(dir) and os.path.getsize(dir+POP_FILE)>0):
        # Get the last row and check if we finished the run
        f = pd.read_csv(dir+POP_FILE)

        last = int(f.tail(1).values.tolist()[0][0])

        if(last  < GENRATIONS):
          lost.append(seed)
          print(dir + '===FOUND===NOGO===' + str(last))

        else:
          print(dir + '===FOUND===FINISHED')

      else:
        print(dir + '===NOGO')
        lost.append(seed)


  print('SEED INCOMPLETE/UNCREATED=', lost)
  print('-----------------------------'*4)
  print()




def main():
  # Generate the arguments
  parser = argparse.ArgumentParser(description="Data aggregation script.")
  parser.add_argument("data_directory", type=str, help="Target experiment directory.")
  parser.add_argument("selection", type=int, help="What selection do we want to check")
  parser.add_argument("generation", type=int, help="What selection do we want to check")


  # Get the arguments
  args = parser.parse_args()
  data_directory = args.data_directory
  sel = args.selection
  gen = args.generation

  print('Starting run_fin_cnt.py')
  print('GENRATIONS=' + str(gen))

  # What are we checking
  if(sel == 0):
    lex(data_directory, gen)

  elif(sel == 1):
    tour(data_directory, gen)

  elif(sel == 2):
    coh(data_directory, gen)

  elif(sel == 3):
    dsl(data_directory, gen)


if __name__ == "__main__":
    main()