[![Build Status](https://travis-ci.org/nrobinson2000/particle-cli-completion.svg?branch=master)](https://travis-ci.org/nrobinson2000/particle-cli-completion)
# particle-cli-completion

<p align="center">
<img src="demo.gif" >
</p>

*Created because of [this request.](https://github.com/spark/particle-cli/issues/369)*

## Load the completion:

```bash
$ source particle
```

**Now try tabbing while using `particle`!**

## Automatic Install:

You can install the completion using the [install script](https://github.com/nrobinson2000/particle-cli-completion/blob/master/install):

```bash
$ bash <(curl -sL https://git.io/vQWZD)
```

## Regenerating particle completion automatically

```bash
$ cd generator
$ python3 completion.py
$ python3 combine.py
$ python3 generate.py > ../particle
```