import express from 'express'
import { createClient } from 'redis'
import { promisify } from 'util'

// Data
const listProducts = [
	{ id: 1 , name: 'Suitcase 250' , price: 50, stock: 4},
	{ id: 2 , name: 'Suitcase 450' , price: 100, stock: 10},
	{ id: 3 , name: 'Suitcase 650' , price: 350, stock: 2},
	{ id: 4 , name: 'Suitcase 1050' , price: 550, stock: 5},
];

// Create redis client
const client = createClient();
// Promisify methods
const promisifiedClientGet = promisify(client.get).bind(client);
const promisifiedClientSet = promisify(client.set).bind(client);
// Functions
const getItemById = (id) => {
	const result = listProducts.find((product) => product.id === id);
	return result;
};

const reserveStockById = async (itemId, stock) => {
	const product = getItemById(itemId);
	const key = `${product.name}.${itemId}`

	await promisifiedClientSet(key, stock);
};

const getCurrentReservedStockById = async (itemId) => {

	const product = getItemById(itemId);
	const key = `${product.itemName}.${itemId}`

	const stock = await promisifiedClientGet(key);
	return stock !== null ? parseInt(stock, 10) : 0;
};

// Express app
const app = express();
const port = 1245;

// Routes
app.get('/list_products', (req, res) => {
	const products = listProducts.map((product) => ({
		itemId: product.id,
		itemName: product.name,
		price: product.price,
		initialAvailableQuantity: product.stock
	}))

	res.json(products);
});

app.get('/list_products/:itemId', async (req, res) => {
	const itemId = parseInt(req.params.itemId, 10);
	const product = getItemById(itemId);

	if (!product) {
		return res.json({"status":"Product not found"});
	}

	const reservedStock = await getCurrentReservedStockById(itemId);
	const availableStock = product.stock - reservedStock;

	res.json({
		itemId: product.id,
		itemName: product.name,
		price: product.price,
		initialAvailableQuantity: product.stock,
		currentQuantity: availableStock
	});
});

app.get('/reserve_product/:itemId', async (req, res) => {
	const itemId = parseInt(req.params.itemId, 10);
	const product = getItemById(itemId);

	if (!product) {
		return res.json({"status":"Product not found"});
	}

	const reservedStock = await getCurrentReservedStockById(itemId);
	const availableStock = product.stock - reservedStock;

	if (availableStock < 1) {
		return res.json({"status":"Not enough stock available","itemId":itemId});
	}

	await reserveStockById(itemId, availableStock - 1);
	res.json({"status":"Reservation confirmed","itemId":itemId});


});

app.listen(port);
