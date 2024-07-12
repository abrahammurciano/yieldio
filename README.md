# yieldio

An async framework implemented only with generators.

I made this project to learn more about how async/await and generators work in Python, and to demonstrate how async/await are really just generators in disguise.

## Example

Take a look at `example.py`, and feel free to run it to see it in action.

```bash
$ python example.py A B C
```

## How to use it

You can use `yieldio` instead of `asyncio` and it works basically the same way, just with generators instead of coroutines. As such, you `yield` instead of `await`. You also don't mark your functions with `async`.

```python
import yieldio

def foo():
	yield yieldio.sleep(1)
	return random.randint(0, 100)

def main():
	print('Hello, world!')
	result = yield foo()
	print(f'foo returned {result}')

yieldio.run(main())
```