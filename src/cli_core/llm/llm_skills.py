
import json


class FaaLLmSkills:




    def __init__(self):
        self.meta = None
        self.skills={}

    def load(self,path:str="./config/skills_config.json"):

        with open(path, 'r') as f:
            self.meta = json.loads(f.read())
            self.skills=self.meta["skills"]
            print(self.skills)
        pass


    def get_all_skill(self):
        return self.skills

    def load_skill(self,skill_name:str):

        skill_path=self.skills.get(skill_name,None)
        if skill_path is None:
            return "skill not found"

        skill_meta=""

        try:
            with open(skill_path, "r", encoding="utf-8") as f:
                skill_meta = f.read()

        except Exception as e:
            return "is not a valid json file"


        return skill_meta
        pass

    def to_str(self):
        return ""


if __name__ == '__main__':
    skills=FaaLLmSkills()
    skills.load()
    skills.load_skill("skill1")
