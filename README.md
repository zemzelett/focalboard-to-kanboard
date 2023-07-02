# Focalboard to Kanboard migration

I've written a blog post if you're interested in a bit more insight.

## How to use

1. Export the individual Focalboard board you wish to migrate to Kanboard.Choose
   the "Export board archive" option.
2. Create a Kanboard board with the same columns as your Focalboard board.
3. Then run the script as follows:

   ```shell
   python3 focal-to-kan.py archive-2023-07-02

   # Or specify an extra output location/filename
   python3 focal-to-kan.py archive-2023-07-02 -o board.csv
   ```

4. Import the CSV into your previously cerated Kanboard board
