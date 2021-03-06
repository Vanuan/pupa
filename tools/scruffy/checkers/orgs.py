from .. import Check
from .common import common_checks


def check(db):
    for org in db.organizations.find({"classification": "legislature"}):
        for check in common_checks(org, 'organization', 'organizations'):
            yield check

        jid = org.get('jurisdiction_id')
        if jid is None:
            yield Check(collection='organizations',
                        id=org['_id'],
                        tagname='org-has-no-jurisdiction',
                        severity='critical')
            continue

        jorgs = list(db.organizations.find({
            "classification": "legislature",
            "jurisdiction_id": org['jurisdiction_id']
        }))
        if len(jorgs) != 1 and len(set([x['chamber']
                                        for x in jorgs])) != len(jorgs):
            yield Check(collection='organizations',
                        id=org['_id'],
                        tagname='jurisdiction_id-has-duped-orgs-by-chamber',
                        severity='critical',
                        data=[[x['chamber'], x['_id']] for x in jorgs
                               if x['chamber'] == org['chamber']])

        if org.get('parent_id'):
            yield Check(collection='organizations',
                        id=org['_id'],
                        tagname='jurisdiction-has-a-parent',
                        severity='important')

        if "/" not in jid:
            yield Check(collection='organizations',
                        id=org['_id'],
                        tagname='jurisdiction-has-no-slashes',
                        severity='grave')
        else:
            prefix, uid = jid.split("/", 1)
            uid, what = uid.rsplit("/", 1)
            if prefix != 'ocd-jurisdiction':
                yield Check(collection='organizations',
                            id=org['_id'],
                            tagname='org-has-bad-jurisdiction-id-prefix',
                            severity='critical')

        if ":" in what:
            yield Check(collection='organizations',
                        id=org['_id'],
                        tagname='org-has-malformed-jurisdiction-id-ender',
                        severity='critical')

        kvp = [f.split(":") for f in uid.split("/")]
        if any((len(x) != 2) for x in kvp):
            yield Check(collection='organizations',
                        id=org['_id'],
                        tagname='org-has-malformed-jurisdiction-id-path',
                        severity='critical')


    for org in db.organizations.find({"classification": "party"}):
        if 'jurisdiction_id' in org and org['jurisdiction_id']:
            yield Check(collection='organizations',
                        id=org['_id'],
                        tagname='party-has-jurisdiction-id',
                        severity='critical',
                        data={
                            "jurisdiction_id": org['jurisdiction_id']
                        })
