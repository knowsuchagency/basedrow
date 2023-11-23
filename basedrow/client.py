import httpx


class Client:
    def __init__(self, url, token):
        self.url = url
        self.token = token
        self.headers = {"Authorization": f"Token {self.token}"}
        self.params = {"user_field_names": True}

        self.client = self.get_client()

    def get_client(self):
        return httpx.Client(
            base_url=self.url,
            headers=self.headers,
            params=self.params,
        )

    def get(self, endpoint, **kwargs) -> dict:
        endpoint = endpoint.lstrip("/") if not endpoint.startswith("http") else endpoint
        resp = self.client.get(endpoint, **kwargs)
        resp.raise_for_status()
        return resp.json()

    def post(self, endpoint, **kwargs) -> dict:
        endpoint = endpoint.lstrip("/") if not endpoint.startswith("http") else endpoint
        resp = self.client.post(endpoint, **kwargs)
        resp.raise_for_status()
        return resp.json()

    def patch(self, endpoint, **kwargs) -> dict:
        endpoint = endpoint.lstrip("/") if not endpoint.startswith("http") else endpoint
        resp = self.client.patch(endpoint, **kwargs)
        resp.raise_for_status()
        return resp.json()

    def list_rows(
        self,
        table_id,
        page=1,
        size=100,
        search: str = None,
        order_by: str = None,
        filters: str = None,
        filter_type: str = None,
        include: str = None,
        exclude: str = None,
        view_id: int = None,
        **kwargs,
    ):
        filter_args = {}

        for k in kwargs.copy():
            if k.startswith("filter__"):
                filter_args[k] = kwargs.pop(k)

        params = {
            "page": page,
            "size": size,
            "search": search,
            "order_by": order_by,
            "filter_type": filter_type,
            "include": include,
            "exclude": exclude,
            "view_id": view_id,
            "filters": filters,
            **filter_args,
        }
        params = {k: v for k, v in params.items() if v is not None}
        return self.get(f"/database/rows/table/{table_id}/", params=params, **kwargs)

    def get_row(self, table_id, row_id):
        return self.get(f"/database/rows/table/{table_id}/{row_id}/")

    def create_rows(self, table_id, rows: list[dict], before: int = None):
        endpoint = f"/database/rows/table/{table_id}/batch/"
        params = {"before": before}
        body = {"items": rows}
        return self.post(endpoint, params=params, json=body)

    def create_row(self, table_id, row: dict, before: int = None):
        return self.post(
            f"/database/rows/table/{table_id}/",
            params={"before": before},
            json=row,
        )

    def update_rows(self, table_id, rows: list[dict]):
        endpoint = f"/database/rows/table/{table_id}/batch/"
        return self.patch(endpoint, json={"items": rows})


class WindmillClient(Client):
    def __init__(self, resource):
        from wmill import get_resource

        r: dict = get_resource(resource) # noqa
        url, token = r["url"], r["token"]
        super().__init__(url, token)


class Table:
    def __init__(self, table_id, client: Client):
        self.table_id = table_id
        self.client = client

    def list_rows(
        self,
        page=1,
        size=100,
        search: str = None,
        order_by: str = None,
        filters: str = None,
        filter_type: str = None,
        include: str = None,
        exclude: str = None,
        view_id: int = None,
        **kwargs,
    ):
        return self.client.list_rows(
            self.table_id,
            page=page,
            size=size,
            search=search,
            order_by=order_by,
            filters=filters,
            filter_type=filter_type,
            include=include,
            exclude=exclude,
            view_id=view_id,
            **kwargs,
        )

    def get_row(self, row_id):
        return self.client.get_row(self.table_id, row_id)

    def create_rows(self, rows: list[dict], before: int = None):
        return self.client.create_rows(self.table_id, rows, before=before)

    def create_row(self, row: dict, before: int = None):
        return self.client.create_row(self.table_id, row, before=before)

    def update_rows(self, rows: list[dict]):
        return self.client.update_rows(self.table_id, rows)
