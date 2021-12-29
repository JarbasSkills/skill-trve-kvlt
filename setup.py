#!/usr/bin/env python3
from setuptools import setup

# skill_id=package_name:SkillClass
PLUGIN_ENTRY_POINT = 'skill-trve-kvlt.jarbasai=skill_trve_kvlt:BlackMetalSkill'

setup(
    # this is the package name that goes on pip
    name='ovos-skill-trve-kvlt',
    version='0.0.1',
    description='ovos black metal skill plugin',
    url='https://github.com/JarbasSkills/skill-trve-kvlt',
    author='JarbasAi',
    author_email='jarbasai@mailfence.com',
    license='Apache-2.0',
    package_dir={"skill_trve_kvlt": ""},
    package_data={'skill_trve_kvlt': ['locale/*', 'ui/*', 'res/*']},
    packages=['skill_trve_kvlt'],
    include_package_data=True,
    install_requires=["ovos_workshop~=0.0.5a1"],
    keywords='ovos skill plugin',
    entry_points={'ovos.plugin.skill': PLUGIN_ENTRY_POINT}
)
