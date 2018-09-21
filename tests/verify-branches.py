import requests
from subprocess import check_output


class TestMicrok8sBranches(object):

    def test_branches(self):
        """
        We need to make sure the LP builders pointing to the master github branch are only pushing to the
        latest and current k8s stable snap tracks. An indication that this is not enforced is that
        we do not have a branch for the k8s release for the previous stable release. Let me clarify
        with an example.

        Assuming upstream stable k8s release is v1.12.x, there has to be a 1.11 github branch used by
        the respective LP builders for building the v1.11.y.

        """
        upstream_version = self._upstream_release()
        assert upstream_version
        version_parts = upstream_version.split('.')
        major_minor_upstream_version = "{}.{}".format(version_parts[0][1:], version_parts[1])
        prev_major_minor_version = "{}.{}".format(version_parts[0][1:], int(version_parts[1])-1)
        print("Current stable is {}. Making sure we have a branch for {}".format(
            major_minor_upstream_version, prev_major_minor_version))
        cmd = "git ls-remote --heads http://github.com/ubuntu/microk8s.git {}".format(prev_major_minor_version)
        branch = check_output(cmd.split())
        assert prev_major_minor_version in branch

    def _upstream_release(self):
        """Return the latest stable k8s in the release series"""
        release_url = "https://dl.k8s.io/release/stable.txt"
        r = requests.get(release_url)
        if r.status_code == 200:
            return r.content.decode().strip()
        else:
            None
