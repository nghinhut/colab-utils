import unittest
from unittest.mock import patch, MagicMock
from colab_utils.bitbucket import (
    get_repo_permissions,
    get_group_users,
    get_repo_info,
    list_repository_permissions,
    Permission,
    Repository
)


class TestBitbucketUtils(unittest.TestCase):

    @patch('bitbucket.requests.get')
    def test_get_repo_permissions(self, mock_get):
        # Mock the API responses
        mock_responses = [
            MagicMock(json=lambda: {'values': [{'user': {'username': 'user1', 'display_name': 'User One'}}]}),
            MagicMock(json=lambda: {'values': [{'group': {'full_slug': 'group1'}}]}),
            MagicMock(json=lambda: {'values': []})
        ]
        mock_get.side_effect = mock_responses

        with patch('bitbucket.get_group_users', return_value=[{'username': 'user2', 'display_name': 'User Two'}]):
            permissions = get_repo_permissions('test-repo')

        self.assertIn('admin', permissions)
        self.assertIn('write', permissions)
        self.assertIn('read', permissions)
        self.assertEqual(permissions['admin'].user['username'], 'user1')
        self.assertEqual(permissions['write'].group['full_slug'], 'group1')
        self.assertEqual(permissions['write'].users[0]['username'], 'user2')

    @patch('bitbucket.requests.get')
    def test_get_group_users(self, mock_get):
        mock_get.return_value.json.return_value = {
            'values': [
                {'username': 'user1', 'display_name': 'User One'},
                {'username': 'user2', 'display_name': 'User Two'}
            ]
        }

        users = get_group_users('test-group')

        self.assertEqual(len(users), 2)
        self.assertEqual(users[0]['username'], 'user1')
        self.assertEqual(users[1]['display_name'], 'User Two')

    @patch('bitbucket.requests.get')
    @patch('bitbucket.get_repo_permissions')
    def test_get_repo_info(self, mock_get_permissions, mock_get):
        mock_get.return_value.json.return_value = {
            'slug': 'test-repo',
            'name': 'Test Repo',
            'description': 'A test repository'
        }
        mock_get_permissions.return_value = {
            'admin': Permission(type='admin', user={'username': 'admin'})
        }

        repo_info = get_repo_info('test-repo')

        self.assertEqual(repo_info['slug'], 'test-repo')
        self.assertEqual(repo_info['name'], 'Test Repo')
        self.assertIn('permissions', repo_info)
        self.assertIn('admin', repo_info['permissions'])

    @patch('bitbucket.get_repo_info')
    def test_list_repository_permissions(self, mock_get_repo_info):
        mock_get_repo_info.return_value = {
            'slug': 'test-repo',
            'name': 'Test Repo',
            'permissions': {
                'admin': {
                    'type': 'admin',
                    'user': {'username': 'admin', 'display_name': 'Admin User'}
                },
                'write': {
                    'type': 'write',
                    'group': {'full_slug': 'test-group'},
                    'users': [
                        {'username': 'user1', 'display_name': 'User One'},
                        {'username': 'user2', 'display_name': 'User Two'}
                    ]
                }
            }
        }

        with patch('builtins.print') as mock_print:
            list_repository_permissions('test-repo')

        mock_print.assert_any_call('Permissions for repository: Test Repo')
        mock_print.assert_any_call('  Admin permission:')
        mock_print.assert_any_call('    User: Admin User (admin)')
        mock_print.assert_any_call('  Write permission:')
        mock_print.assert_any_call('    Group: test-group')
        mock_print.assert_any_call('    Users in group:')
        mock_print.assert_any_call('      - User One (user1)')
        mock_print.assert_any_call('      - User Two (user2)')

if __name__ == '__main__':
    unittest.main()