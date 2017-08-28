## PyPatent


### File structure 
* PyPatent (dir)
  - **main.py**
  - **readpatentpdf.py**
  - **readabstracttxt.py**
  - TEXT_Files (dir containing initial data)
     * Patent 1 & literature searches (dir)
     *  ...
     * Patent N & literature searches (dir)
 - Train (dir containing pre-processed data) 
     * **abstract2vec.py**
     * **a2v.d2v** (the trained model)
     * training txt files converted from patents and abstracts   

### How to run PyPatent?

1. Clone or fork this repository
2. Create a Python enviornment with the repo's `requirements.txt` libraries (e.g. `conda create -n pypatent python=3.5 anaconda --file requirements.txt`)
3. Activate that enviornment (`source activate pypatent`)
4. Run `main.py` from the project directory(`(pypatent) computer:PyPatent hclent$ python main.py`)
    * This will produce a `results.csv` file, with the results.   


### Debugging?
After you run the code once, there will be a `.pypatent.log` file, which an help you if anything has gone amiss. 


