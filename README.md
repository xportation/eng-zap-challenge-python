# Opção B: Fazer uma API (backend)

Coloque essa lógica numa API backend, onde dada a **origem do portal** em uma _request_ o seu _response_ 
será a **listagem dos imóveis**. O _routing_ da aplicação fica a seu gosto.  
  
O payload da _response_, além de conter a lista de imóveis com o contrato de _output_, **deve conter** os 
seguintes metadados de paginação e totais, implementar esses metadados é **obrigatório**:
```json
  {
    pageNumber: int32,
    pageSize: int32,
    totalCount: int32,
    listings: [
      ...
    ]
  }
```
Faça essa API pensando que ela pode ser consumida por vários tipos de clientes e com diferentes 
propósitos - portanto implemente o que mais achar relevante e que faça sentido.  
  
Você deverá usar como source o `source-2` ou `source-2.json` (~10000 registros):

- `http://grupozap-code-challenge.s3-website-us-east-1.amazonaws.com/sources/source-2.json`
- `http://grupozap-code-challenge.s3-website-us-east-1.amazonaws.com/sources/source-2`


# Regras
- Um imóvel não é elegível em NENHUM PORTAL se:  
  - Ele tem lat e lon iguais a 0.
- Caso o imóvel seja para venda, ele é elegível para o portal ZAP se:
  - O valor do metro quadrado (chave usableAreas) não pode ser menor/igual a R$ 3.500,00 - apenas considerando imóveis que tenham usableAreas acima de 0 (imóveis com usableAreas = 0 não são elegíveis).
  - Quando o imóvel estiver dentro do bounding box dos arredores do Grupo ZAP (descrito abaixo) considere a regra de valor mínimo (do imóvel) 10% menor.
- Caso o imóvel seja para aluguel, ele é elegível para o portal Viva Real se:
  - O valor do condomínio não pode ser maior/igual que 30% do valor do aluguel - apenas aplicado para imóveis que tenham um monthlyCondoFee válido e numérico (imóveis com monthlyCondoFee não numérico ou inválido não são elegíveis).
  - Quando o imóvel estiver dentro do bounding box dos arredores do Grupo ZAP (descrito abaixo) considere a regra de valor máximo (do aluguel do imóvel) 50% maior.

## Onde
```json
{
  ...
  updatedAt: "2016-11-16T04:14:02Z", // data de atualização do imóvel
  address: {
    geolocation: {
      location: { // latitude/longitude do imóvel
        "lon": -46.716542,
        "lat": -23.502555
      },
    },
  },
  pricingInfos: {
    monthlyCondoFee: "495"
  }
}
```
## Bounding Box Grupo ZAP
```
minlon: -46.693419
minlat -23.568704
maxlon: -46.641146
maxlat: -23.546686
```

# Database Model Sample
```json
  {
    "usableAreas": 69,
    "listingType": "USED",
    "createdAt": "2016-11-16T04:14:02Z",
    "listingStatus": "ACTIVE",
    "id": "some-id",
    "parkingSpaces": 1,
    "updatedAt": "2016-11-16T04:14:02Z",
    "owner": false,
    "images": [
      "https://resizedimgs.vivareal.com/crop/400x300/vr.images.sp/some-id1.jpg",
      "https://resizedimgs.vivareal.com/crop/400x300/vr.images.sp/some-id2.jpg",
      "https://resizedimgs.vivareal.com/crop/400x300/vr.images.sp/some-id3.jpg",
      "https://resizedimgs.vivareal.com/crop/400x300/vr.images.sp/some-id4.jpg",
      "https://resizedimgs.vivareal.com/crop/400x300/vr.images.sp/some-id5.jpg"
    ],
    "address": {
      "city": "",
      "neighborhood": "",
      "geoLocation": {
        "precision": "ROOFTOP",
        "location": {
          "lon": -46.716542,
          "lat": -23.502555
        }
      }
    },
    "bathrooms": 2,
    "bedrooms": 3,
    "pricingInfos": {
      "yearlyIptu": "0",
      "price": "405000",
      "businessType": "SALE",
      "monthlyCondoFee": "495"
    }
  }
```
