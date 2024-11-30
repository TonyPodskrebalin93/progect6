import unittest
import logging

import home_work_12_4 as ts


class RunnerTest(unittest.TestCase):

    def test_walk(self):
        try:
            walker = ts.Runner("Anton", - 5)
            for _ in range(10):
                walker.walk()
            self.assertEqual(walker.distance, 50)
            logging.info('"test_walk" выполнен успешно')
        except ValueError as err:
            logging.error("Неверная скорость для Runner", exc_info=True)

    def test_run(self):
        try:
            run = ts.Runner(123)
            for _ in range(10):
                run.run()
                self.assertEqual(run.distance, 100)
                logging.info('"test_run" выполнен успешно')
        except TypeError as err:
            logging.error("Неверный тип данных для объекта Runner", exc_info=True)

    def test_challenge(self):
        walker2 = ts.Runner('Vasily')
        run2 = ts.Runner('Sergey')
        for i in range(10):
            walker2.walk()
            run2.run()
        self.assertNotEqual(run2.distance, walker2.distance)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, filemode="w", filename="runner_tests.log", encoding="UTF-8",
                        format="%(asctime)s | %(levelname)s | %(message)s")
    unittest.main()