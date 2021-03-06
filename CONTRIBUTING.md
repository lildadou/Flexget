Issues
======

If you are looking for help, rather than reporting a problem, please use the [forum.](http://discuss.flexget.com)

Before submitting an issue, make sure you:

- Are running the latest version of FlexGet (check `flexget --version`)
- Check if there is already an issue open about the problem.
- Fully describe the problem, explain what you expected to happen.
- Include the relevant config of the task having the trouble. (Remember to censor private info though.)
- Include log segments (especially if there are tracebacks.) Remember to censor private info from these as well.
  Sometimes debug logs may be needed as well `flexget --debug execute --tasks my_problem_task`
- Surround your config and log segments with 3 backticks ```` ``` ```` so that they are made into proper code blocks:

        ```

        <config or log here>

        ```

Pull Requests
=============

For help, see GitHub's guides on [forking a repo](https://help.github.com/articles/fork-a-repo/) and
[pull requests.](https://help.github.com/articles/using-pull-requests/)

When submitting pull requests:

- Submit PRs against the [develop](https://github.com/Flexget/Flexget/tree/develop) branch.
- Explain in your PR the bug you are fixing or feature you are adding. Reference ticket numbers if relevant.
- If config changes are needed, mention those as well. They will be needed for the
  [UpgradeActions](http://flexget.com/wiki/UpgradeActions) page upon merging anyway.
- Make separate PRs for separate ideas. The smaller each PR is the easier it is to get it reviewed and merged.
  You don't want a bugfix to get held up by a new feature you also added.


Wiki
====

Updating the wiki is also a valuable way to contribute. The wiki can be found at <http://flexget.com>
