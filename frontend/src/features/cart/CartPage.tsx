 import { Button, Paper, Card, Stack, Text, Title, Group, Loader, Alert } from "@mantine/core";
import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom"
import { http } from "../../services/http";

type cartItem = {
    row_id: string;
    household_id: string;
    item_id: string;
    item_name: string;
    quantity: string;
    unit: string;
    is_bought: boolean;
};

type cartListResponse = {
    cart: cartItem[];
};

export default function CartPage() {
    const navigate = useNavigate();
    const { householdid } = useParams();
    const [error, setError] = useState("");
    const [items, setItems] = useState<cartItem[]>([]);
    const [loading, setLoading] = useState(true);
    async function addItem() {
        try {
            navigate(`/households/${householdid}/cart/add`)
            console.log("Added item to cart.")

        } catch {
            console.log("Unable to add item to cart.")
        }
    }

    // Retreive items from Inventory for display
    useEffect(() => {
        async function loadInventory() {
            try {
                setError("");
                const response = await http.get<cartListResponse>(`/households/${householdid}/cart/all`);
                setItems(response.data.cart);

            } catch {
                setError("Could not load your cart.")

            } finally {
                setLoading(false);
            }
        }
        loadInventory();
    }, [])

    // Async func to delte item from inventory
    async function deleteItem(row_id: string) {
        try {
            await http.delete(`/households/${householdid}/cart/${row_id}`);
            setItems((prevItems) => prevItems.filter((item) => item.row_id !== row_id));

        } catch {
            console.log("Failed to delete")
        }

    }
    return (
        <main className="page">
            <Paper withBorder shadow="md" radius="xl" p="xl" maw={760} mx="auto">
                <Stack gap="lg">
                    <div>
                        <Text c="green.7" fw={700} tt="uppercase" size="sm">
                            Grocery App
                        </Text>
                        <Title order={1}> Cart </Title>
                        <Text c="dimmed">
                            Edit the cart as per requirements.
                        </Text>
                    </div>
                

                {loading ? (
                    <Group>
                        <Loader size="sm"/>
                        <Text c="dimmed">Loading items...</Text>
                    </Group>
                ): null}

                {error ? (
                    <Alert color="red" title="Could not load cart">
                        {error}
                    </Alert>
                ): null}

                {!loading && !error && items.length === 0 ? (
                    <Card withBorder radius="lg" p="lg">
                        <Text c="dimmed" mt={4}>
                            Add an item to cart for a great shopping experience.
                        </Text>
                    </Card>
                ): null}

                <Stack gap="sm">
                    {items.map((item) => 
                    <Card
                    key={item.row_id}
                    withBorder
                    radius="lg"
                    p="md"
                    >
                        <Group justify="space-between" align="center">
                            <div>
                                <Text fw={700}>{item.item_name}</Text>
                                <Text>{item.quantity} {item.unit}</Text>
                            </div>
                            <Button onClick={() => deleteItem(item.row_id)} size="sm" radius="md" color="red">Delete</Button>
                        </Group>
                    </Card>)}
                </Stack>

                <Button 
                fullWidth
                radius="xl"
                variant="filled"
                color="green"
                onClick={addItem}>
                    Add new item
                </Button> 
            </Stack>
            </Paper>
        </main>
    )
}