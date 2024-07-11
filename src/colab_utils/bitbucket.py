import os
import json
import requests
import concurrent.futures
import logging
from typing import List, Optional, Dict, Any
from dataclasses import dataclass, field
from datetime import datetime

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Environment variables
BITBUCKET_USERNAME = os.getenv('BITBUCKET_USERNAME')
BITBUCKET_APP_PASSWORD = os.getenv('BITBUCKET_APP_PASSWORD')
BITBUCKET_API_BASE = 'https://api.bitbucket.org/2.0'


@dataclass
class Link:
    href: str


@dataclass
class RepositoryLinks:
    source: Link
    clone: Link
    self: Link


@dataclass
class CloneLink:
    name: str
    href: str


@dataclass
class Owner:
    display_name: str
    type: str
    uuid: str
    username: str
    links: Dict[str, Dict[str, str]] = field(default_factory=dict)


@dataclass
class Workspace:
    type: str
    uuid: str
    name: str
    slug: str
    links: Dict[str, Dict[str, str]] = field(default_factory=dict)


@dataclass
class Project:
    type: str
    key: str
    uuid: str
    name: str
    links: Dict[str, Dict[str, str]] = field(default_factory=dict)


@dataclass
class MainBranch:
    name: str
    type: str


@dataclass
class OverrideSettings:
    default_merge_strategy: bool
    branching_model: bool


@dataclass
class Permission:
    type: str
    user: Optional[Dict[str, Any]] = None
    group: Optional[Dict[str, Any]] = None
    users: List[Dict[str, Any]] = field(default_factory=list)
    source: Optional[str] = None


@dataclass
class Repository:
    type: str
    full_name: str
    name: str
    slug: str
    description: str
    scm: str
    website: str
    owner: Owner
    workspace: Workspace
    is_private: bool
    project: Project
    fork_policy: str
    created_on: datetime
    updated_on: datetime
    size: int
    language: str
    uuid: str
    mainbranch: MainBranch
    override_settings: OverrideSettings
    has_issues: bool
    has_wiki: bool
    links: RepositoryLinks
    parent: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        # Convert string dates to datetime objects
        data['created_on'] = datetime.fromisoformat(data['created_on'].rstrip('Z'))
        data['updated_on'] = datetime.fromisoformat(data['updated_on'].rstrip('Z'))

        # Create nested objects
        data['owner'] = Owner(**data['owner'])
        data['workspace'] = Workspace(**data['workspace'])
        data['project'] = Project(**data['project'])
        data['mainbranch'] = MainBranch(**data['mainbranch'])
        data['override_settings'] = OverrideSettings(**data['override_settings'])

        return cls(**data)


def get_repo_info(repo_slug: str, workspace: str) -> Dict[str, Any]:
    url = f"{BITBUCKET_API_BASE}/repositories/{workspace}/{repo_slug}"
    response = requests.get(url, auth=(BITBUCKET_USERNAME, BITBUCKET_APP_PASSWORD))
    response.raise_for_status()
    return response.json()


def download_file(url: str, filename: str) -> None:
    response = requests.get(url, auth=(BITBUCKET_USERNAME, BITBUCKET_APP_PASSWORD))
    response.raise_for_status()
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'wb') as f:
        f.write(response.content)


def get_file_urls(repo_info: Dict[str, Any], file_patterns: List[str]) -> List[tuple]:
    base_url = repo_info['links']['source']['href']
    main_branch = repo_info['mainbranch']['name']
    return [
        (f"{base_url}/{main_branch}/{pattern}", f"{repo_info['slug']}/{pattern}")
        for pattern in file_patterns
    ]


def download_repo_files(repo_slug: str, file_patterns: List[str]) -> None:
    try:
        repo_info = get_repo_info(repo_slug)
        urls_and_filenames = get_file_urls(repo_info, file_patterns)

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(download_file, url, filename) for url, filename in urls_and_filenames]
            concurrent.futures.wait(futures)
    except requests.exceptions.HTTPError as e:
        logger.error(f"Failed to get repo info for {repo_slug}: {e}")


def download_all_repo_files(repo_slugs: List[str], file_patterns: List[str]) -> None:
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(download_repo_files, repo_slug, file_patterns) for repo_slug in repo_slugs]
        for future in concurrent.futures.as_completed(futures):
            future.result()

    logger.info("Downloaded all required files.")


def parse_repositories(json_string: str) -> List[Repository]:
    # Parse the JSON string into a Python object
    data = json.loads(json_string)

    # Create a list of Repository objects
    repositories = [Repository.from_dict(repo_data) for repo_data in data]

    return repositories
