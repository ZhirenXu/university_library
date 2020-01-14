import unittest
from package import login_def

class TestLogin(unittest.TestCase):

    def test_Json_website(self):
        print("start testing...")
        loginLink = "https://webauth.service.ohio-state.edu/idp/profile/SAML2/Redirect/SSO?execution=e3s1"
        jsonLink = "https://library.osu.edu/dc/catalog?f%5Badmin_set_sim%5D%5B%5D=biclm+migrated+collections&locale=en&search_field=all_fields"
        login_def.login(jsonLink, loginLink)


if __name__ == '__main__':
    unittest.main()
