from sharepoint import get_sharepoint_sites


try:
    data = get_sharepoint_sites()

    print("SharePoint connection successful!")

    sites = data.get("value", [])

    print(f"Sites found: {len(sites)}")

    for site in sites:
        print(
            f"- {site.get('displayName', 'Unnamed Site')}"
        )

except Exception as e:
    print("SharePoint connection failed:")
    print(e)