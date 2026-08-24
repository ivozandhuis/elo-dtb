# echo "=== run python script" 
# cd ../additions
# ./familyname_phonetics.py

# cd ../qlever

# echo "=== collect data" 

# find ../additions/normalizations -name '*.nt.gz' | xargs cat > data/normalizations.nt.gz

echo "=== do clever"
sudo qlever -q qleverfiles/Qleverfile start
sudo qlever -q qleverfiles/Qleverfile ui