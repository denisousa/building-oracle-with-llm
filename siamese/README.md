## Tutorial to Execute Siamese
## Notes
- The project works exclusively for Ubuntu
- You can make project settings in the .env file
- If you want to do quick tests, use `mini_qualitas_corpus_clean` which is downloaded together with the other datasets.
- Another way to do quick experiments is to use `parameters_grid_search_mini.yml` which is a smaller version of the parameters used for grid_search.

### 1. Remove the requirement to use Sudo
Run the command `sudo visudo` and make the following changes
```bash
sudo visudo
```

Insert at the end of the file
```bash
<your-user> ALL=(ALL) NOPASSWD: ALL
```

### 2. Configure Java context to Siamese
```bash
chmod +x java-install.sh
./java-install.sh
```

### 3. Download Qualitas Corpus, StackOverflow and Elasticsearch datasets
```bash
python download_datasource.py
```

### 4. Execute Siamese to perform indexing
```bash
python siamese_indexing.py
```

### 8. Execute experiment
```bash
python siamese_search.py
```

