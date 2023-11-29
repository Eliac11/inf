import unittest
from main import factorial, is_palindrome

class TestModul(unittest.TestCase):

    def test_positive_numbers(self):
        self.assertEqual(factorial(0), 1)
        self.assertEqual(factorial(1), 1)
        self.assertEqual(factorial(5), 120)
        self.assertEqual(factorial(10), 3628800)

    def test_negative_number(self):
        with self.assertRaises(ValueError):
            factorial(-1)

    def test_non_integer_input(self):
        with self.assertRaises(ValueError):
            factorial(3.5)

    def test_string_input(self):
        with self.assertRaises(TypeError):
            factorial("abc")

    def test_large_number(self):
        with self.assertRaises(RecursionError):
            factorial(1000)

    def test_valid_palindromes(self):
        self.assertTrue(is_palindrome("A man a plan a canal Panama"))
        self.assertTrue(is_palindrome("Able was I ere I saw Elba"))
        self.assertTrue(is_palindrome("Was it a car or a cat I saw"))

    def test_invalid_palindromes(self):
        self.assertFalse(is_palindrome("Hello, World!"))
        self.assertFalse(is_palindrome("OpenAI GPT-3"))
        self.assertFalse(is_palindrome("This is not a palindrome"))

    def test_empty_string(self):
        self.assertTrue(is_palindrome(""))

    def test_single_character(self):
        self.assertTrue(is_palindrome("a"))

    def test_case_sensitive(self):
        
        self.assertTrue(is_palindrome("AbBa"))
        self.assertFalse(is_palindrome("Abbaa"))
    
    def test_case_int(self):
        with self.assertRaises(AttributeError):
            is_palindrome(234234)

if __name__ == '__main__':
    unittest.main()
