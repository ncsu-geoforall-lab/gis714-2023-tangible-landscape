# NCSU GIS 714 Spring 2023: Tangible Landscape

## How to add a new activity

To add a new activity to this project, you need to fork this repository, create a branch, create a pull request,
and, of course, develop your new activity. The following sections go over the specific steps.
A later section discusses how to modify an action later on using another pull request.

### Set up your repository

To be able to create pull request (PR), you will need to set up a fork
and a local repository on your computer
(to make changes and to test code locally):

1. Fork this repository on GitHub.
   - In the web interface, there is a _Fork_ button.
1. Clone your fork on your computer.
   - For example, in the command line, use the `git clone` command:
     `git clone {url-of-the-repo}`

### Develop new analysis

1. Create a new Python script according to the provided example.
   - There is an example called `simple_example.py` in the `activities` directory
     which gives information about the specific conventions.
   - Use a unique filename, for example use your name (e.g., `petras.py`).
   - Jupyter can be used to create the file, alternatively, you can use the
     Simple Python Editor in GRASS GIS.
1. Develop a new analysis and write it as a function in the file.
1. Test your analysis locally on your computer or in Binder.
   - Use the NC SPM sample location for GRASS GIS.

Place the file in the `activities` directory. If the file is not in the
`activities` directory or if it does not have the
`.py` extension, it will be ignored by the automated system.

### Configure an activity

1. Create a new JSON configuration file according to the provided example.
   - There is an example called `simple_example.json` in the `activities` directory
     which provides an example of a minimal activity configuration.
   - Again, use a unique filename, for example use your name (e.g., `petras.json`).
   - Use Jupyter to create the file or your favorite text editor.
1. Set value for the `analyses` key to the filename of your Python script.
1. Modify `layers` to fit your needs.
1. Change `title`, `author`, and `instructions` for the task to best describe your work.

Note that the name of the JSON configuration file should differ from the name of the
Python file only by extension (`.json` versus `.py`).

### Create a pull request

Once you have your new files ready, you can do all the Git related steps
(you could do them as your are working, too).

We will use Git in command line here and for creating the PR with GitHub web interface,
but you can use any Git desktop tool including GitHub Desktop.
You can also do all through the GitHub web interface.
(On the other hand, if you want to do everything in command line, you can add GitHub CLI to the mix.)
Notably, you can't do this from the online Binder environment
(Binder recommends not to enter any credentials in their environment).

Create a new branch for your changes and switch to it.
Here, we will call the new branch `add-awesome-activity`.
In command line, do:

```sh
git switch -c add-awesome-activity
```

Add Python script with your Python file and your JSON file to the repository
as new files:

```sh
git add activities/awesome-activity.py
git add activities/awesome-activity.json
```

Record the changes:

```sh
git commit -m "Add awesome activity"
```

Publish the changes into your fork
(`origin` is how Git refers to the remote repository you cloned from,
`add-awesome-activity` is the name you have picked earlier for your branch):

```sh
git push origin add-awesome-activity
```

This will give your URL to create pull request on GitHub
or simply go to GitHub and it will suggest you to open a PR.

## After opening PR

After you open a PR, you will see various checks running at the bottom of
the PR page. The checks are testing correctness of the code from several
perspectives including syntax, indentation, and several checks specific to
this repository.

If you see _Some checks were not successful_, review the output to
see the details of what is wrong.
For example, if you see the _Super-Linter_ check failing, click _Details_
and then scroll up to see the actual error which, in this case, can be
recognized by the word _ERROR_.

Result of one of these checks needs to be examined manually.
Its name is _Render activities_ and it is running the Python file and
combining it with the associated JSON file into an HTML page.
So, even when the check says _Successful_, click on _Details_ next to its name,
then _Summary_ on the left, and then in _Artifacts_ at the bottom,
download the _activities-as-html_ artifact,
unzip it, find an HTML file named like your JSON file
and open it in your web browser. You should see the title you provided
and the rendering of your results according to what you specified
in the JSON file. This provides you with the idea of what will
eventually happen in Tangible Landscape.

You can run any of these checks locally as well, but it is more practical to just
start using some of the basic tools used in the background,
namely _Black_, _Flake8_, and _Pylint_.
For the rest, you can just rely on the checks associated with the PR.

If some of the checks are failing for you or the _activities-as-html_ artifact
does not look as you intended, make required changes locally, do `git add`, then commit and push
as you did before. This will update the PR and trigger the checks.
Repeat as needed.

## How to modify your activity

When your PR is merged, the main, original repository is updated.
Here, we will refer to this repository as the _upstream repository_.
What was updated in the upstream repository was the `main` branch
which will be important in a moment.

Because the changes from the PR are now in the `main` branch
of the upstream repository, modifying your Tangible Landscape activity
now requires that you update your fork first.

### Update your fork

To update your fork using a combination of the GitHub web interface and command line,
go to your fork and switch to the _main_ branch using a combo box on the left.
Then push the _Fetch and merge_ button on the right (confirm the action if needed).
Then locally in command line, you can do:

```sh
git switch main
git pull
```

Your local _main_ branch should now be the same as the one in the upstream repository
and you should be ready to create a new branch for futher updates.

Alternatively, to update your fork using only command line,
first, you need to add the upstream repository as another
_remote repository_ to the clone on your local machine.

So, add the upstream repository as another remote repository called `upstream`.
In command line, using:

```sh
git remote add upstream https://github.com/ncsu-geoforall-lab/gis714-2023-tangible-landscape
```

Second, switch to the `main` branch of your repository
(the `main` branch should have no changes in it since you used a separate branch
to make the changes for your first PR):

```sh
git switch main
```

Third, update the `main` branch of your local repository to match
the `main` branch from the upstream repository.
This can be done with the two following commands:

```sh
git fetch upstream
git rebase upstream/main
```

### Make and publish changes

Now when your local `main` branch is up to date with the `main` branch
of the upstream repository,
you can just follow the instructions above for creating a new activity,
in short, you need to:

1. create a new branch (you can also do it after you make the changes),
2. make changes,
4. add changes to Git,
5. make commits,
6. publish (push) the changes online, and
7. create a pull request.
