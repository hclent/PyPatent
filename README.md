## PyPatent


### File structure 
* PyPatent (dir)
  - **main.py**
  - **readpatentpdf.py**
  - **readabstracttxt.py**
  - Patent\_Literature\_Search\_Pairs (dir)
     * Patent 1 & literature searches (dir)
     *  ...
     * Patent N & literature searches (dir)
 - Train (dir)
     * **abstract2vec.py**
     * training txt files from patents and abstracts   

### How to run PyPatent?
Assuming you have the data ...

1. Create a Python enviornment with the `requirements.txt` libraries (e.g. `conda create -n pypatent python=3.5 anaconda --file requirements.txt`)
2. Activate that enviornment (`source activate pypateent`)
3. Run main.py from the project directory(`(pypatent) computer:PyPatent heather$ python main.py`)   


### Debugging?
After you run the code once, there will be a `.pypatent.log` file, which an help you if anything has gone amiss. 
