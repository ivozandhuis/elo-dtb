find ../../etl/dtb_trouwen/serialized -name '*.nt.gz' | xargs cat > elo_dtb_trouwen.nt.gz
find ../../etl/dtb_dopen/serialized -name '*.nt.gz' | xargs cat > elo_dtb_dopen.nt.gz

# find ../../additions/improvements -name '*.nt.gz' | xargs cat > improvements.nt.gz
# find ../../additions/normalizations -name '*.nt.gz' | xargs cat > normalizations.nt.gz