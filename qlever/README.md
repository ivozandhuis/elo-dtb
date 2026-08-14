# Qlever

To run a qlever instance with the data (necessary for the additions-steps) 

0. install qlever
See: [documentation](https://docs.qlever.dev/quickstart/)

1. collect data from the etl and the additions directory

```
cd data
./data-collector.sh
```

2. do the qlever steps

```
cd ../qlever
sudo qlever -q qleverfiles/Qleverfile index
sudo qlever -q qleverfiles/Qleverfile start
sudo qlever -q qleverfiles/Qleverfile ui
```

If you already had an earlier instance running:

```
cd ../qlever
sudo qlever -q qleverfiles/Qleverfile stop
sudo qlever -q qleverfiles/Qleverfile index --overwrite-existing
sudo qlever -q qleverfiles/Qleverfile start
sudo qlever -q qleverfiles/Qleverfile ui
```