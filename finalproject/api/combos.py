from typing import Protocol

from fastapi import APIRouter, Depends, HTTPException
from fastapi.requests import Request
from pydantic import BaseModel

from finalproject.models.campaigns import ComboItem, Combo
from finalproject.service.combos import ComboService
from finalproject.service.exceptions import ComboNotFound
from finalproject.store.combo import ComboStore
from finalproject.store.combo_item import ComboItemStore
from finalproject.store.product import ProductStore

combos_api = APIRouter()

class _Distributor(Protocol):
    def products(self) -> ProductStore:
        pass
    
    def combos(self) -> ComboStore:
        pass

    def combo_items(self) -> ComboItemStore:
        pass
    
class ComboRequest(BaseModel):
    name: str
    items: list[ComboItem]
    discount: float


class SingleComboResponse(BaseModel):
    combo: Combo


class ListCombosResponse(BaseModel):
    combos: list[Combo]
    
def get_combo_service(
        request: Request
) -> ComboService:
    distributor: _Distributor = request.app.state.distributor
    return ComboService(
        distributor.products(),
        distributor.combos(),
        distributor.combo_items(),
    )

@combos_api.get(
    "/",
    status_code=200,
    response_model=ListCombosResponse,
)
def list_combos(
    campaign_service: ComboService = Depends(get_combo_service),
) -> ListCombosResponse:
    combos = campaign_service.get_all_combos()
    return ListCombosResponse(combos=combos)


@combos_api.post(
    "/",
    status_code=201,
    response_model=SingleComboResponse,
)
def add_combo(
    combo_request: ComboRequest,
    campaign_service: ComboService = Depends(get_combo_service),
) -> SingleComboResponse:
    combo = Combo(
        id="",
        name=combo_request.name,
        items=combo_request.items,
        discount=combo_request.discount,
    )
    campaign_service.add_combo(combo)
    return SingleComboResponse(combo=combo)


@combos_api.get(
    "/{combo_id}",
    status_code=200,
    response_model=SingleComboResponse,
)
def get_combo(
    combo_id: str,
    campaign_service: ComboService = Depends(get_combo_service),
) -> SingleComboResponse:
    try:
        combo = campaign_service.get_combo(combo_id)
        return SingleComboResponse(combo=combo)
    except ComboNotFound:
        raise HTTPException(status_code=404, detail="Combo not found")


@combos_api.patch(
    "/{combo_id}",
    status_code=200,
    response_model=None,
)
def remove_combo(
    combo_id: str,
    campaign_service: ComboService = Depends(get_combo_service),
) -> None:
    try:
        campaign_service.remove_combo(combo_id)
    except ComboNotFound:
        raise HTTPException(status_code=404, detail="Combo not found")