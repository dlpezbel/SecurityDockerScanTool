import unittest

from project.service.dockerfile_service import DockerfileParser, DockerfileService


class Dockerfile_Service_Test(unittest.TestCase):

    def test_given_a_dockerfile_when_parse_then_instructions_are_parsed(self):
        parser = DockerfileParser('test/resources/Dockerfile_test1')
        instructions = parser.structure()
        self.assertEqual(len(instructions), 4)
        self.assertEqual(instructions.__getitem__(0).get("instruction"), 'FROM')
        self.assertEqual(instructions.__getitem__(1).get("instruction"), 'RUN')
        self.assertEqual(instructions.__getitem__(0).get("value"), 'alpine:3.4')

    def test_given_an_empty_dockerfile_when_parse_then_instructions_is_empty(self):
        parser = DockerfileParser('test/resources/Dockerfile_empty')
        instructions = parser.structure()
        self.assertEqual(len(instructions), 0)

    def test_given_a_dockerfile_with_comments_when_parse_then_comments_are_not_parsed(self):
        parser = DockerfileParser('test/resources/Dockerfile_test2')
        instructions = parser.structure()
        self.assertEqual(len(instructions), 5)
        self.assertEqual(instructions.__getitem__(0).get("instruction"), 'FROM')
        self.assertEqual(instructions.__getitem__(0).get("value"), 'alpine:3.4')
        self.assertEqual(instructions.__getitem__(1).get("instruction"), 'RUN')
        self.assertEqual(instructions.__getitem__(2).get("instruction"), 'COMMENT_INSTRUCTION')

    def test_given_a_dockerfile_without_user_when_check_then_KO(self):
        result = DockerfileService.check_dockerfile(self,'test/resources/Dockerfile_test2')
        user_check_result = list(filter(lambda x: x['4_1']['evaluation'] == 'KO', result))
        self.assertEqual(len(user_check_result),1)

    def test_given_a_dockerfile_with_user_when_check_then_OK(self):
        result = DockerfileService.check_dockerfile(self,'test/resources/Dockerfile_with_user')
        user_check_result = list(filter(lambda x: x['4_1']['evaluation'] == 'OK', result))
        self.assertEqual(len(user_check_result),1)

    def test_given_a_dockerfile_without_user_when_check_and_fix_then_KO(self):
        result = DockerfileService.check_and_fix_dockerfile(self,'test/resources/Dockerfile_test2')
        user_check_result = list(filter(lambda x: x['4_1']['evaluation'] == 'KO', result))
        self.assertEqual(len(user_check_result),1)

    def test_given_a_dockerfile_with_user_when_check_and_fix_then_OK(self):
        result = DockerfileService.check_and_fix_dockerfile(self,'test/resources/Dockerfile_with_user')
        user_check_result = list(filter(lambda x: x['4_1']['evaluation'] == 'OK', result))
        self.assertEqual(len(user_check_result),1)

    def test_given_a_dockerfile_without_user_when_fix_then_instruction_with_user_is_generated(self):
        instructions = DockerfileService.parse_dockerfile(self,'test/resources/Dockerfile_test2')
        check_result = DockerfileService.evaluate_dockerfile(self, instructions)
        result = DockerfileService.get_dockerfile_fixes(self, check_result)
        user_instruction = list(filter(lambda x: x['instruction'] == 'USER', result))
        user_add_instruction = list(filter(lambda x: x['instruction'] == 'RUN' and x['value'].startswith( 'useradd' ), result))
        self.assertEqual(len(user_instruction),1)
        self.assertEqual(len(user_add_instruction),1)

    def test_given_a_dockerfile_with_user_when_check_and_fix_then_OK(self):
        result = DockerfileService.check_and_fix_dockerfile(self,'test/resources/Dockerfile_with_user')
        user_check_result = list(filter(lambda x: x['4_1']['evaluation'] == 'OK', result))
        self.assertEqual(len(user_check_result),1)

    def test_given_a_dockerfile_without_healthcheck_when_fix_then_instruction_with_healthcheck_is_generated(self):
        instructions = DockerfileService.parse_dockerfile(self,'test/resources/Dockerfile_test2')
        check_result = DockerfileService.evaluate_dockerfile(self, instructions)
        result = DockerfileService.get_dockerfile_fixes(self, check_result)
        healthcheck_instruction = list(filter(lambda x: x['instruction'] == 'HEALTHCHECK', result))
        self.assertEqual(len(healthcheck_instruction),1)

if __name__ == '__main__':
    unittest.main()