# FSD-2024
Financial Systems Design Repository 2024

# Cloning the Repository

To get started with the Financial Systems Design Repository 2024, follow these simple steps to clone the repository to your local machine:

1. **Install Git**: Ensure that Git is installed on your system. You can download and install Git from [here](https://git-scm.com/), if you haven't already.

2. **Open Terminal/Command Prompt**: Open your terminal or command prompt on your computer.

3. **Navigate to Desired Directory**: Navigate to the directory where you want to clone the repository. You can do this using the `cd` command. For example:
   ```bash
   cd /path/to/your/directory
   ```

4. **Clone the Repository**: Use the `git clone` command followed by the repository's URL. Replace `<repository_URL>` with the URL of your repository. For example:
   ```bash
   git clone <repository_URL>
   ```

5. **Access the Repository**: Once the cloning process is complete, navigate into the repository directory using the `cd` command. For example:
   ```bash
   cd FSD-2024
   ```

You can now find and all the files within the repository directory. You can explore its contents, make changes, and contribute as needed.


# Creating a Virtual Environment

A virtual environment in Python allows you to create isolated environments for different projects, keeping dependencies separate and avoiding conflicts. To create a virtual environment, you can use the built-in `venv` module, which comes with Python 3.3 and later. First, navigate to your project directory in the terminal. Then, run the following command:

```
python3 -m venv myenv
```

Replace `myenv` with the desired name for your virtual environment. This command creates a new directory named `myenv` containing a copy of Python interpreter and a `site-packages` directory for installing packages. To activate the virtual environment, use the appropriate command for your operating system:

- On Windows:

```
myenv\Scripts\activate
```

- On Unix or MacOS:

```
source myenv/bin/activate
```

Once activated, you'll see the name of the virtual environment in your terminal prompt. Now you can install packages without affecting the global Python installation. To deactivate the virtual environment, simply type `deactivate` in the terminal.

# Installing Requirements from `requirements.txt`

When working on a Python project, it's common to have a `requirements.txt` file listing all the dependencies required for your project. To install these dependencies, navigate to your project directory in the terminal where your `requirements.txt` file is located. Then, run the following command:

```
pip install -r requirements.txt
```

This command tells pip to install all the packages listed in the `requirements.txt` file. Each line in the file represents a package, optionally with a specified version or other constraints. Pip will automatically resolve dependencies and install the required packages into your current Python environment. This approach ensures that everyone working on the project has the same dependencies installed, making it easier to manage and share code.

# Creating a Branch

After cloning the Financial Systems Design Repository 2024 to your local machine, you may want to create a new branch to work on your changes. Follow these steps to create a new branch:

1. **Navigate to Repository Directory**: Open your terminal or command prompt and navigate into the cloned repository directory using the `cd` command. For example:
   ```bash
   cd FSD-2024
   ```

2. **Create a New Branch**: Use the `git checkout` command followed by the `-b` option and the name of your new branch. For example, to create a branch named `feature-branch`:
   ```bash
   git checkout -b feature-branch
   ```

3. **Verify Branch Creation**: You can verify that the branch has been created by using the `git branch` command. It will list all branches, with an asterisk (*) indicating the current branch:
   ```bash
   git branch
   ```

Now you have successfully created a new branch named `feature-branch` and switched to it. You can start making your changes and commits on this branch without affecting the main branch.


